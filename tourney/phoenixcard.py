from django.db import connections
from decimal import Decimal

# cursor = connections['hi'].cursor()

class PhoenixCard:
    def __init__(self, cardno=None, rfid=None):

        self.cursor = connections['hi'].cursor()
        self._validate_number(cardno, rfid)
        # verify cardno and rfid combination
        r = self._verify(cardno, rfid)
        self.cardno = str(r['cardno'])
        self.rfid = str(r['rfid'])
        self.org_rfid = str(r['org_rfid'])

        # set card info
        (card_type, rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
                m_num, utime, f_name, l_name, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr) = self._card_info()

        self.nick_name = name
        self.user_id = m_id

        self.first_name = f_name
        self.last_name = l_name
        self.gender = m_sex
        self.email = m_email
        self.phone = m_phone
        self.zip = m_zip

        self.ppd = ppd
        self.mpr = mpr

        self.card_type = card_type
        self.is_copied = False if self.rfid == self.org_rfid else True
        self.is_new = True if self.card_type == 'new' else False

    def __str__(self):
        return self.cardno if self.cardno else self.rfid

    def _validate_number(self, cardno, rfid):
        # check card number format
        if not cardno and not rfid:
            raise Exception('cardno or rfid needs to be set')
        else:
            if cardno and (len(str(cardno)) != 16 or not str(cardno).isdigit()):
                raise Exception('card number format is invalid: %s' % [cardno])
            if rfid and (len(str(rfid)) != 20 or not str(rfid).isdigit()):
                raise Exception('rfid format is invalid: %s' % [rfid])

    def _verify(self, cardno, rfid):
        cursor = self.cursor
        try:
            cursor.execute('SELECT cardno, rfid, getorigrfid2(%s) from checkrfid where cardno=%s or rfid=%s', [rfid, cardno, rfid])
            r = cursor.fetchone()
        except Exception, e:
            raise Exception('db error: %s' % [e])
        if not r:
            raise Exception('Casual card variflication failed')
        (cardno, rfid, org_rfid ) = r
        return {'cardno': cardno, 'rfid': rfid, 'org_rfid': org_rfid}

    def _card_info(self):
        """Get card info.
        There are 5 different card types:
        1. blank/never used new one
            no userinfo (name is null), no members(m_num is null)  and utime is null
        2. used on console but not registered on the web
            userinfo record but no members(m_num is null) and utime is still null
        3. registered as a principal card

        4. registered as an extra card

        5. copied card

        """
        cursor = self.cursor
        rfid = self.rfid
        try:
            cursor.execute("""SELECT %s, (select cardno from checkrfid where rfid=%s),
                                a.cardno, a.rfid, b.rfid, c.rfid, name, m_num, utime,
                                realname, m_sex, m_email, m_phone, m_id, m_zip, ppd_ta2, mpr_ta2
                                FROM checkrfid a
                                LEFT JOIN userinfo b on a.rfid=b.rfid
                                LEFT JOIN members c on b.m_num=c.num
                                LEFT JOIN useravg d on b.rfid=d.rfid
                                WHERE a.rfid=getorigrfid2(%s)""", [rfid, rfid, rfid])

            (rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
             m_num, utime, realname, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr) = cursor.fetchone()
        except Exception, e:
            raise Exception('card variflication failed: %s' % [e])

        if m_sex == 1:
            m_sex = 'F'
        elif m_sex == 2:
            m_sex = 'M'
        else:
            m_sex = ''

        if realname:
            names = realname.split()
            if len(names) == 1:
                f_name = names[0]
                l_name = ''
            elif len(names) == 2:
                f_name = names[0].strip()
                l_name = names[1].strip()
            elif len(names) >= 3:
                f_name = names[0].strip()
                l_name = names[2].strip()
        else:
            f_name = ''
            l_name = ''

        m_email = m_email.strip().lower() if m_email else ''

        ppd = ppd if ppd else Decimal(0)
        mpr = mpr if mpr else Decimal(0)

        if not userinfo_rfid and not members_rfid and not utime:
            # blank, never used one
            card_type = 'new'
        elif userinfo_rfid and name and not m_num and not utime:
            # used on console but not registered on the web
            card_type = 'temporary'
        elif (userinfo_rfid == members_rfid) and m_num and m_id:
            # principal card
            card_type = 'principal'
        elif (userinfo_rfid != members_rfid) and m_num and m_id:
            card_type = 'extra'

        return (card_type, rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
                m_num, utime, f_name, l_name, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr)


    def get_stat(self):
        cursor = self.cursor
        cursor.execute('SELECT ppd_ta2, mpr_ta2 from useravg where rfid=getorigrfid2(%s)', [self.rfid,])
        (ppd, mpr) = cursor.fetchone()
        return {'PPD': ppd, 'MPR': mpr}


class PhoenixLeagueCard(PhoenixCard):
    def __init__(self, cardno=None, rfid=None):
        self.cursor = connections['hi'].cursor()

        self._validate_number(cardno, rfid)
        r = self._verify(cardno, rfid)

        self.cardno = str(r['cardno'])
        self.rfid = str(r['rfid'])

        (name, nickname, ppd_ta, mpr_ta) = self._card_info()
        self.ppd = ppd_ta
        self.mpr = mpr_ta
        self.nick_name = nickname
        self.name = name

    def _verify(self, cardno, rfid):
            cursor = self.cursor
            try:
                cursor.execute('SELECT cardno, rfid from lg_checkrfid where cardno=%s or rfid=%s', [cardno, rfid])
                r = cursor.fetchone()
            except Exception, e:
                raise Exception('card variflication failed: %s' % [e])
            if not r:
                raise Exception('League card variflication failed')
            (cardno, rfid) = r
            return {'cardno': cardno, 'rfid': rfid}

    def _card_info(self):
        cursor = self.cursor
        cursor.execute('SELECT name, nickname, ppd_ta, mpr_ta from ml.luser a, ml.luserinfo b where a.rfid=b.rfid and a.rfid=%s', [self.rfid,])
        (name, nickname, ppd_ta, mpr_ta) = cursor.fetchone()
        return (name, nickname, ppd_ta, mpr_ta)
