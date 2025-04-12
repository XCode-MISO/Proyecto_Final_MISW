import firebase_admin
from firebase_admin import auth, exceptions

def registrarUsuarioEnFirebase(correo, rol):
    try:
        user_record = auth.create_user(email=correo)
        claims = {"role": rol}
        auth.set_custom_user_claims(user_record.uid, claims)
        return user_record.uid
    except exceptions.FirebaseError as e:
        print(f"Firebase error: {e}")
        return None
    except ValueError as e:
        print(f"Value error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None