from .errors import FieldRequired, FieldInvalid, FieldOneof

class Validator:


    def czy_nip_prawidlowy(self):
        return True


    def h_good_int(self,field, fieldName):
        if field is None:
            raise FieldRequired(fieldName)
        try:
            f = int(field)
            if f < 0:
                raise FieldInvalid("wartość pola " + fieldName + " nie może byc ujemna")
            return str(f)
        except:
            raise FieldInvalid(fieldName)


    def h_required(self,field, fieldName):
        if field is None:
            raise FieldRequired(fieldName)
        return field


    def h_oneof(self,field, lmap, fieldName):
        if field is None:
            raise FieldRequired(fieldName)
        if not field in lmap:
            raise FieldOneof("TODO: wybór jeden z:" + str(','.join(lmap.values())))
        return lmap[field]


