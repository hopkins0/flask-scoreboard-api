from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
 
engine = create_engine('postgresql+psycopg2://bocauser:boca@localhost/bocadb', echo=True)
Base = declarative_base(engine)
########################################################################
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


#----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 

def get_info_active_contest(session = None):
    if session == None :
        return None
    return session.query(ContestTable).filter(ContestTable.contestactive == True).one()

# sql = "select * from usertable where contestnumber=:contest_number and usertype='team' and userlastlogin is not null and userenabled='t'";
def get_user_for_contest(session, active_contest):
    return session.query(UserTable).filter(UserTable.contestnumber == active_contest,
            UserTable.usertype == 'team', UserTable.userlastlogin.isnot(None), 
            UserTable.userenabled == True).all()


# "select r.usernumber as user, p.problemname as problemname, r.runproblem as problem, ".
# "p.problemcolor as color, p.problemcolorname as colorname, " .
# "r.rundatediff as time, r.rundatediffans as anstime, a.yes as yes, r.runanswer as answer "

# "from runtable as r, answertable as a, problemtable as p "

# "where r.runanswer=a.answernumber and " .
# "a.contestnumber=$contest 
# and p.problemnumber=r.runproblem 
# and p.contestnumber=$contest 
# and " .
# # "r.contestnumber=$contest 
# and r.runsitenumber=$site 
# and (r.runstatus ~ 'judged' or r.runstatus ~ 'judged+') and " .
# # "r.rundatediff>=0 
# and r.rundatediff<=$tf 
# and r.rundatediffans<=$ta " . 

# "order by r.usernumber, r.runproblem, r.rundatediff", "DBScoreSite(get runs)");


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

def get_score_all(session, active_contest):
    return session.query(RunTable, AnswerTable, ProblemTable) \
            .join(AnswerTable) \
            .join(ProblemTable) \
            .filter(RunTable.runanswer == AnswerTable.answernumber) \
            .filter(AnswerTable.contestnumber == active_contest) \
            .filter(ProblemTable.problemnumber == RunTable.runproblem) \
            .filter(ProblemTable.contestnumber == active_contest) \
            .filter(RunTable.contestnumber == active_contest) \
            .filter(RunTable.rundatediff >= 0) \
            .order_by(RunTable.usernumber) \
            .order_by(RunTable.runproblem) \
            .order_by(RunTable.rundatediff)


if __name__ == "__main__":
    session = loadSession()
    
    active_contest = get_info_active_contest(session)

    user_table = get_user_for_contest(session, active_contest.contestnumber)
    

    site_table = session.query(SiteTable).filter(SiteTable.contestnumber == active_contest.contestnumber).one()
    # select * from sitetable where sitenumber=$site and contestnumber=$contest";

    score_site = get_score_all(session, active_contest.contestnumber)


    i = 0
    print "==============================="
    for r in score_site:
        if i == 0:
            print "\n\nuser, problemname, problem, " + \
                "color, colorname, " + \
                "time, anstime, yes, answer "
        i = i + 1
        print "===============>>"
        print r.RunTable.usernumber, r.ProblemTable.problemname, r.RunTable.runproblem, \
            r.ProblemTable.problemcolor, r.ProblemTable.problemcolorname, \
            r.RunTable.rundatediff, r.RunTable.rundatediffans, r.AnswerTable.yes, r.RunTable.runanswer, \
            r.RunTable.runstatus

    print "[END] ==================== [END]"
    print i