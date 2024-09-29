import streamlit as st
from utils.common import initialize

def home():
    initialize("Home")

    st.title("SamoPrezentacja")

    st.markdown("Kompleksowa ocena Twoich wystąpień!")
    st.markdown("Wykorzystaj moc sztucznej inteligencji, aby analizować, oceniać \
                i doskonalić swoje umiejętności wystąpień. Prześlij wideo, a \
                „SamoPrezentacja” dostarczy Ci w czasie rzeczywistym wgląd w klarowność, \
                emocje i ogólną jakość wypowiedzi. Gotowy, by zmienić sposób, w \
                jaki się prezentujesz?"
    )

    st.write("\n")
    st.write("\n")

    st.write("Rozpocznij teraz: Przejdź do sekcji 'Upload'.")


if __name__ == "__main__":
    home()
