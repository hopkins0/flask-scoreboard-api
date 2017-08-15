from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_


from app import Base
from app import engine



class ContestTable(Base):
    """"""
    __tablename__ = 'contesttable'
    __table_args__ = {'autoload':True}


class UserTable(Base):
    """"""
    __tablename__ = 'usertable'
    __table_args__ = {'autoload':True}
 


class RunTable(Base):
    """"""
    __tablename__ = 'runtable'
    __table_args__ = {'autoload':True}

class AnswerTable(Base):
    """"""
    __tablename__ = 'answertable'
    __table_args__ = {'autoload':True}

class ProblemTable(Base):
    """"""
    __tablename__ = 'problemtable'
    __table_args__ = {'autoload':True}


class SiteTable(Base):
    __tablename__ = 'sitetable'
    __table_args__ = {'autoload':True}

class SiteTimeTable(Base):
    __tablename__ = 'sitetimetable'
    __table_args__ = {'autoload':True}




#----------------------------------------------------------------------

from sqlalchemy import inspect

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

#----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 

def get_info_active_contest(session):
    return session.query(ContestTable).filter(ContestTable.contestactive == True).one()


def get_user_for_contest(session, active_contest):
    return session.query(UserTable).filter(UserTable.contestnumber == active_contest,
            UserTable.usertype == 'team', UserTable.userlastlogin.isnot(None), 
            UserTable.userenabled == True).order_by(UserTable.usernumber).all()



def get_score_judged(session, active_contest):
    return session.query(RunTable, AnswerTable, ProblemTable) \
            .join(AnswerTable) \
            .join(ProblemTable) \
            .filter(RunTable.runanswer == AnswerTable.answernumber) \
            .filter(AnswerTable.contestnumber == active_contest) \
            .filter(ProblemTable.problemnumber == RunTable.runproblem) \
            .filter(ProblemTable.contestnumber == active_contest) \
            .filter(RunTable.contestnumber == active_contest) \
            .filter(or_(RunTable.runstatus == 'judged', RunTable.runstatus == 'judged+')) \
            .filter(RunTable.rundatediff >= 0) \
            .order_by(RunTable.usernumber) \
            .order_by(RunTable.runproblem) \
            .order_by(RunTable.rundatediff)

def get_runs_all(session, active_contest, run_number = 0):
    return session.query(RunTable, AnswerTable, ProblemTable) \
            .join(AnswerTable) \
            .join(ProblemTable) \
            .filter(RunTable.runanswer == AnswerTable.answernumber) \
            .filter(AnswerTable.contestnumber == active_contest) \
            .filter(ProblemTable.problemnumber == RunTable.runproblem) \
            .filter(ProblemTable.contestnumber == active_contest) \
            .filter(RunTable.contestnumber == active_contest) \
            .filter(RunTable.rundatediff >= 0) \
            .filter(RunTable.runnumber >= run_number) \
            .order_by(RunTable.runnumber) \
            .order_by(RunTable.usernumber) \
            .order_by(RunTable.runproblem) \
            .order_by(RunTable.rundatediff)



def get_all_problems(session, active_contest):
    return session.query(ProblemTable)\
            .filter(ProblemTable.fake != 't')\
            .filter(ProblemTable.contestnumber == active_contest) \
            .filter(ProblemTable.problemfullname != '(DEL)') \
            .order_by(ProblemTable.problemnumber)
    


import time
def get_site_info_contest(session):
    active_contest = get_info_active_contest(session)
    sites = session.query(SiteTable)\
            .filter(SiteTable.contestnumber == active_contest.contestnumber).all()

    a = object_as_dict(next(iter(sites or []), None))
    
    sites_time = session.query(SiteTimeTable)\
                .filter(SiteTimeTable.contestnumber == active_contest.contestnumber) \
                .order_by(SiteTimeTable.sitestartdate)

    a['currenttime'] = 0
    a['siterunning'] = False;
    a['siteenddate'] = 0
    a['sitestartdate'] = 0
    ti = int(time.time())

    index = 0
    for b in sites_time:
        if index == 0:
            a['sitestartdate'] = b.sitestartdate

        if b.siteenddate == 0:
            a['siterunning'] = True
            a['currenttime'] = a['currenttime'] + ti - b.sitestartdate
        else:
            a['currenttime'] = a['currenttime'] + b.siteenddate - b.sitestartdate
        a['siteenddate'] = b.siteenddate

    if a['siteenddate'] == 0:
        a['siteenddate'] = ti - a['siteduration'] - a['currenttime']
    
    a['siteautoended'] = False
    if a['siteautoend'] == False and a['currenttime'] >= a['siteduration']:
        a['siterunning'] = False
        a['siteautoended'] = True

    return a

def get_site_clock(session):
    s = get_site_info_contest(session)

    if s['siteactive'] == False:
        return {'msg': 'no esta activo', 'active': False}
    if s['siterunning'] == False:
        return {'msg': 'no esta corriendo', 'active': False}

    if s['currenttime'] < 0:
        return {'active': True,
                'running': False,
                'msg': 'Falta para iniciar',
                'time': s['currenttime']}

    if s['currenttime'] >= 0:
        t = s['siteduration'] - s['currenttime']
        return {'active': True,
                'running': True,
                'msg': 'tiempo restante',
                'time': t
                }
    else:
        return {'active': True,
                'running': False,
                'msg': 'no ha iniciado',
                'time': -1}

