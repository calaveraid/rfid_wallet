import RPi.GPIO as GPIO
import mfrc522

MIFAREReader = mfrc522.MFRC522()
defaultKey = [0xFF for k in range(6)]
trailerData = [0xFF, 0x07, 0x80, 0x69]
data = {i:[ord(' ') for j in range(16)] for i in range(4,36)}
trailerBlock = [i for i in range(7,36,4)]
continua = True

try:
    print('\nGrabación de Recovery Phrase en tarjeta RFID')
    print('============================================')
    while continua:
        rawInput = input('\nIntroduce las 24 palabras separadas por espacios: ')
        recPhrase = rawInput.split()
        password = input('\nIntroduce la nueva contraseña (6 caracteres): ')
        password = password[0:6]
        oldPassword = input('\nIntroduce la antigua contraseña (Deja en blanco para tarjetas nuevas): ')
        oldPassword = oldPassword[0:6]

        print('\nComprueba que todos los datos sean correctos:\n')
        for i in range(len(recPhrase)//2):
            print('{:2d}. {:10s} {:2d}. {:10s}'.format(i+1, recPhrase[i], i+13, recPhrase[i+12]))
        print('\nNueva contraseña:   {}'.format(password))
        print('Antigua contraseña: {}'.format(oldPassword))

        confirm = input('\nIntroduce CORRECTO para continuar:\n')

        if confirm == 'CORRECTO':
            continua = False

    continua = True

    #Preparando claves
    if len(oldPassword):
        key = []
        for char in oldPassword:
            key.append(ord(char))
    else:
        key = defaultKey
    
    if len(password):
        newPass = []
        for char in password:
            newPass.append(ord(char))
    else:
        newPass = defaultKey

    #Trailer Blocks
    for indice in trailerBlock:
        data[indice] = newPass + trailerData + newPass
    
    #Preparando bloques de datos
    indice = 4
    for palabra in recPhrase:
        if indice in trailerBlock:
            indice += 1
        for i in range(len(palabra)):
            data[indice][i] = ord(palabra[i])
        indice += 1

    print('\nAcerca tarjeta...')
    
    #Grabando tarjeta
    while continua:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_SelectTag(uid)
            
            print('\nGrabando tarjeta...')
            for block in data:
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)

                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Write(block, data[block])
                    print("Bloque {:2d} grabado".format(block))

                else:
                    print("Error de autenticación")
                    break    

            MIFAREReader.MFRC522_StopCrypto1()
            continua = False
            GPIO.cleanup()
            print('\nListo')

except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nInterrupcion por teclado.\n')
