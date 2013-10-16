from django.db import connections, transaction

class PhoenixCard:
    def __init__(self, cardno=None, rfid=None):
        if not cardno and not rfid:
            raise Exception('cardno or rfid needs to be set')
        else:
            if cardno and (len(str(cardno)) != 16 or not str(cardno).isdigit()):
                raise Exception('invalid card number')
            if rfid and (len(str(rfid)) != 20 or not str(rfid).isdigit()):
                raise Exception('invalid rfid')
            self.cardno = cardno
            self.rfid = rfid
        self.cursor = connections['hi'].cursor()

    def __str__(self):
        return self.cardno if self.cardno else self.rfid

    def get_cardno(self):
        if self.cardno:
            return self.cardno
        elif self.rfid:
            try:
                self.cursor.execute('SELECT cardno from checkrfid where rfid=%s', [self.rfid])
                r = self.cursor.fetchone()
            except Exception:
                raise Exception('invalid rfid number')
            if r:
                return str(r[0])
            else:
                raise Exception('invalid rfid number')
        else:
            raise Exception('cardno or rfid needs to be set')

    def get_rfid(self):
        if self.rfid:
            return self.rfid
        elif self.cardno:
            try:
                self.cursor.execute('SELECT rfid from checkrfid where cardno=%s', [self.cardno])
                r = self.cursor.fetchone()
            except Exception:
                raise Exception('invalid card number')
            if r:
                return str(r[0])
            else:
                raise Exception('invalid card number')
        else:
            raise Exception('cardno or rfid needs to be set')

    def get_stat(self):
        try:
            self.cursor.execute('SELECT ppd_ta2, mpr_ta2 from useravg a, checkrfid b where a.rfid=getorigrfid2(b.rfid) and (b.cardno=%s or b.rfid=getorigrfid2(%s))', [self.cardno, self.rfid])
            r = self.cursor.fetchone()
        except Exception, e:
            raise Exception('invalid card:%s' % [e])
        if r:
            return {'PPD': r[0], 'MPR': r[1]}
        else:
            raise Exception('invalid card')

    def is_new(self):
        try:
            self.cursor.execute('SELECT rfid from userinfo  where cardno=%s or rfid=getorigrfid2(%s)', [self.cardno, self.rfid])
            r = self.cursor.fetchone()
        except Exception, e:
            raise Exception('Invalid card:%s' % [e])
        return True if r == None else False

class PhoenixLeagueCard(PhoenixCard):
   
    def get_cardno(self):
        if self.cardno:
            return self.cardno
        elif self.rfid:
            cursor = connections['hi'].cursor()
            try:
                cursor.execute('SELECT cardno from lg_checkrfid where rfid=%s', [self.rfid])
                r = cursor.fetchone()
            except Exception:
                raise Exception('invalid rfid number')
            if r:
                return str(r[0])
            else:
                raise Exception('invalid rfid number')
        else:
            raise Exception('cardno or rfid needs to be set')

    def get_rfid(self):
        if self.rfid:
            return self.rfid
        elif self.cardno:
            cursor = connections['hi'].cursor()
            try:
                cursor.execute('SELECT rfid from lg_checkrfid where cardno=%s', [self.cardno])
                r = cursor.fetchone()
            except Exception:
                raise Exception('invalid card number')
            if r:
                return str(r[0])
            else:
                raise Exception('invalid card number')
        else:
            raise Exception('cardno or rfid needs to be set')

    def get_stat(self):
        cursor = connections['hi'].cursor()
        try:
            cursor.execute('SELECT ppd_ta, mpr_ta from ml.luser a, lg_checkrfid b where a.rfid=getorigrfid2(b.rfid) and (b.cardno=%s or b.rfid=%s)', [self.cardno, self.rfid])
            r = cursor.fetchone()
        except Exception, e:
            raise Exception('invalid card:%s' % [e])
        if r:
            return {'PPD': r[0], 'MPR': r[1]}
        else:
            raise Exception('invalid card')