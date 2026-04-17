import unittest
import myform_mail

class TestEmail(unittest.TestCase):

    def test_uncorrect_email(self):
        list_mail_uncor = [
            "",
            "1",
            "cat@gmail..com",
            "@mail.com",
            "nastyarozina221@gmail.c",
            "nastyarozina221@gmail",
            "cat@.com",
            "nastyarozrozrozrozrozrozrrrozhinaaaaa@gmail.com",
            ".cat@gmail.com",
            "nasta rozina@gmail.com",
            "nastyarozina221#gmail.com",
            "nas..rozina@gmail.com",
            "nasнrozina@gmail.com"
        ]

        for mail in list_mail_uncor:
            self.assertFalse(myform_mail.check_email(mail))


    def test_correct_email(self):
        list_mail_cor = [
            "row@rg.com",
            "arc@dev.gmail.com",
            "toster@mail-server.com",
            "cat-chudik@mail.com",
            "cat_177@mail.kz",
            "nastya.rozina@yandex.ru",
            "nas.tya-rozhina@gmail.com",
            "nastyarozina221@gmail.com"
        ]

        for mail in list_mail_cor:
            self.assertTrue(myform_mail.check_email(mail))

if __name__ == "__main__":
    unittest.main()