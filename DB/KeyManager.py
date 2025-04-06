import string

class KeyManager:
    def __init__(self):
        self.encryption_key = self.generate_encryption_key(1)
        self.decryption_key = self.generate_encryption_key(0)
    def generate_encryption_key(self, modo):
        abecedario = string.ascii_letters + string.digits + string.punctuation + " "
        
        valores = [
            'fH}yc', 'oUBJ;', 'X1>Cb', '98&-`', 'QwEVu', 'h.Q^A', 'ph|P(', 'rw<]*', 
            'sAN#6', 'bEMEI', 'SnAd-', 'x5]fx', '7z+Dn', '3teZB', 'l0&FZ', 'CN?ZR', 
            'DYEBo', '`@iCF', 'adj2M', 'LDd44', 'UcZ-4', '4iVj*', 'BFjG*', '~Rdqr', 
            ']_foo', '7NOsB', '<jxvE', 'tZn$Q', 'k[_.P', '?aEBC', 'AFdB_', '2t:Jx', 
            'wRyw[', 'c9ef"', '(:N)M', 'mkJa6', '=Ud`A', '>s#7#', '&v3s|', '5z0b3', 
            'zYY7C', '&+LTj', '+tq}8', '?.j8D', 'E@R(^', 'GbBFm', 'wyoir', '9CE2J', 
            '>f|d;', '01G!o', 'eO.Sw', 'i&dhS', '!+qCB', 'b.E/X', 'dC_VE', 'gWRcN', 
            'k2&K,', 'mA7b"', 'oSB&C', 'sYKJd', 'u=Fj5', 'wWA2c', 'yZ<-g', 'Nr6UN', 
            's*<1b', 'rk2P`', ',%hjb', 'Pp2--', 'b@ET.', '1(Y^W', 'E~L:A', 'pl.@K', 
            'OW-70', 'f5"D$', 'AwBcf', '33pEA', 'A",!F', '4VfQ;', 'Dq(iC', 'uZKGc', 
            'l.t>j', ':vp&t', '0)jTB', '}L~Dt', '9N:]a', 'vAEeT', '<yBWf', 'DDHcV', 
            '9d{pn', '}[K=A', 'b.Q5P', 'pF1fZ', 'BQ=Xs', '-eIx?', 'S6EGH', 'fCIJ@', 
            'b*UhQ', 'e5CC~', 'fF_B=', 'xF??o', 'dgIBi', '*S;=v', 'D0vf`', 'Aa!*1', 
            'G(Xi/', 'cz2ad', 'zXLa+', '2BmE@'
        ]

        dictionary = [letra for letra in abecedario]
        if modo == 1:
            key = {letra: valor for letra, valor in zip(dictionary, valores)}
        else:
            key = {valor: letra for letra, valor in zip(dictionary, valores)}
        return key




