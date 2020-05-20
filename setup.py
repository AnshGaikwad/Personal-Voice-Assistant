# Hi There!
# This python script is written to
# install some python modules using
# pip. You can go through the code.

import subprocess
import sys
import get_pip

# Installing Function
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


# Installing gtts
try:
    print("[Script] Trying to import gtts")
    import gtts
except:
    print("[EXCEPTION] gtts not installed")

    try:
        print("[Script] Trying to install gtts via pip")
        import pip

        install("gtts")
        print("[Script] gtts has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[Script] Trying to install pip")
        get_pip.main()
        print("[Script] Pip has been installed")
        try:
            print("[Script] Trying to install gtts")
            import pip

            install("gtts")
            print("[Script] gtts has been installed")
        except:
            print("[ERROR 1] gtts could not be installed")

# Installing wikipedia
try:
    print("[Script] Trying to import wikipedia")
    import wikipedia
except:
    print("[EXCEPTION] wikipedia not installed")

    try:
        print("[Script] Trying to install wikipedia via pip")
        import pip

        install("wikipedia")
        print("[Script] wikipedia has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[Script] Trying to install pip")
        get_pip.main()
        print("[Script] Pip has been installed")
        try:
            print("[Script] Trying to install wikipedia")
            import pip

            install("wikipedia")
            print("[Script] wikipedia has been installed")
        except:
            print("[ERROR 1] wikipedia could not be installed")

# Installing webbrowser
try:
    print("[Script] Trying to import webbrowser")
    import webbrowser
except:
    print("[EXCEPTION] webbrowser not installed")

    try:
        print("[Script] Trying to install webbrowser via pip")
        import pip

        install("webbrowser")
        print("[Script] webbrowser has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[Script] Trying to install pip")
        get_pip.main()
        print("[Script] Pip has been installed")
        try:
            print("[Script] Trying to install webbrowser")
            import pip

            install("webbrowser")
            print("[Script] webbrowser has been installed")
        except:
            print("[ERROR 1] webbrowser could not be installed")

# Installing pyttsx3
try:
    print("[Script] Trying to import pyttsx3")
    import pyttsx3
except:
    print("[EXCEPTION] pyttsx3 not installed")

    try:
        print("[Script] Trying to install pyttsx3 via pip")
        import pip

        install("pyttsx3")
        print("[Script] pyttsx3 has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[Script] Trying to install pip")
        get_pip.main()
        print("[Script] Pip has been installed")
        try:
            print("[Script] Trying to install pyttsx3")
            import pip

            install("pyttsx3")
            print("[Script] pyttsx3 has been installed")
        except:
            print("[ERROR 1] pyttsx3 could not be installed")

# Installing playsound
try:
    print("[Script] Trying to import playsound")
    import playsound
except:
    print("[EXCEPTION] playsound not installed")

    try:
        print("[Script] Trying to install playsound via pip")
        import pip

        install("playsound")
        print("[Script] playsound has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[Script] Trying to install pip")
        get_pip.main()
        print("[Script] Pip has been installed")
        try:
            print("[Script] Trying to install playsound")
            import pip

            install("playsound")
            print("[Script] playsound has been installed")
        except:
            print("[ERROR 1] playsound could not be installed")


# Installing pytz
try:
    print("[Script] Trying to import pytz")
    import pytz
except:
    print("[EXCEPTION] pytz not installed")

    try:
        print("[Script] Trying to install pytz via pip")
        import pip

        install("pytz")
        print("[Script] pytz has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[Script] Trying to install pytz")
        get_pip.main()
        print("[Script] Pip has been installed")
        try:
            print("[Script] Trying to install pytz")
            import pip

            install("pytz")
            print("[Script] pytz has been installed")
        except:
            print("[ERROR 1] pytz could not be installed")

# Installing speech_recognition
try:
    print("[Script] Trying to import speech_recognition")
    import speech_recognition
except:
    print("[EXCEPTION] speech_recognition not installed")

    try:
        print("[Script] Trying to install speech_recognition via pip")
        import pip

        install("speech_recognition")
        print("[Script] speech_recognition has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[Script] Trying to install speech_recognition")
        get_pip.main()
        print("[Script] Pip has been installed")
        try:
            print("[Script] Trying to install speech_recognition")
            import pip

            install("speech_recognition")
            print("[Script] speech_recognition has been installed")
        except:
            print("[ERROR 1] speech_recognition could not be installed")
