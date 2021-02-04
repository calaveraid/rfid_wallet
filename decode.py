import RPi.GPIO as GPIO
import mfrc522

MIFAREReader = mfrc522.MFRC522()
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
data = {i:[] for i in range(4,36)}
trailerBlock = [i for i in range(7,36,4)]
continua = True
recPhrase = []
error = 0

try:
    print('\nLectura de Recovery Phrase en tarjeta RFID')
    print('============================================')
    password = input('\nIntroduce la contraseña (en blanco para Default): ')
    password = password[0:6]

    if len(password):
        key = []
        for char in password:
            key.append(ord(char))
            
    print('\nAcerca tarjeta...')
    while continua:
    
        #Leyendo tarjeta
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_SelectTag(uid)

            continua = False
            print('\nLeyendo tarjeta...')
            for block in data:
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)

                if status == MIFAREReader.MI_OK:
                    data[block] = MIFAREReader.MFRC522_Read(block)

                else:
                    print("Error de autenticación")
                    error = 1
                    break
            
            MIFAREReader.MFRC522_StopCrypto1()
            continua = False
            GPIO.cleanup()
    if not error:
        for indice in data:
            if indice not in trailerBlock:
                word = ''
                for byte in data[indice]:
                    word = word + chr(byte)
                recPhrase.append(word.strip())

        print('\nRecovery Phrase:\n')
        for i in range(len(recPhrase)//2):
            print('{:2d}. {:10s} {:2d}. {:10s}'.format(i+1, recPhrase[i], i+13, recPhrase[i+12]))
        print('\nListo.')

except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nInterrupcion por teclado.\n')
