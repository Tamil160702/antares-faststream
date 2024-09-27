import sys
from neo4j import GraphDatabase

sys.path.append("./../")
from config.config import Config
import os
from neo4j import GraphDatabase, basic_auth


def getneo4j_db():
    # Connect to Neo4j database
    neo4j_host=Config.Neo4j.host
    neo4j_user=Config.Neo4j.user
    neo4j_password=Config.Neo4j.password
    all=[ 
        neo4j_host,
        neo4j_user,
        neo4j_password]

    return all


neo4j_drive = getneo4j_db()
driver = GraphDatabase.driver(neo4j_drive[0],auth=(neo4j_drive[1],neo4j_drive[2]))


async def create_node(msg):
    print("creating node")    
    print(msg)
    user = msg['parentname']
    print(f"user => {user}")
    title =msg['owner']
    print(f"title => {title}")
    
    with driver.session() as session:
        
        # tx = await session.begin_transaction().run("MATCH (u:User {username: $username}) RETURN u", username=user)
        # print(tx)
        # session = session.begin_transaction()
        # Check if the parent user exists
        print("session is connected")
        user_result = session.run("MATCH (u:User {username: $username}) RETURN u", username=user)
        print("check 0")
        user_records = [record.data() for record in user_result]
        print("check 1")
        task_check = session.run("MATCH (c:Task {title: $title}) RETURN c", title=title)
        task_exists = [record.data() for record in task_check]
        print("check 2")
        task_check = session.run("MATCH (c:Task {title: $title}) RETURN c", title=user)
        user_exists = [record.data() for record in task_check]
        print("check 3")
        
        if not user_records  and not task_exists and not user_exists and user and title:
            session.run("CREATE (u:User {username: $username}) RETURN u", username=user)
            task_check = session.run("MATCH (c:Task {title: $title}) RETURN c", title=title)
            task_exists = [record.data() for record in task_check]

            # If the child task does not exist, create it and link to the parent task or user
            if not task_exists:
                session.run(
                    """
                    MATCH (p:User {username: $parentname})
                    CREATE (s:Task {title: $title})
                    MERGE (p)-[:Sub_Assign]->(s)
                    RETURN s
                    """,
                    parentname=user,
                    title=title
                )
            return{
                "parent created and label is assigned to parent"
            }
        if user is None and title:
            session.run("CREATE (u:User {username: $username}) RETURN u", username=title)
            return{
                "parentname is none so we using label to create node"
            }
        elif user is None and title is None:
            return{"there is no values in parent and label"}
        elif user and title is None:
            return{"there is no values in label"}

        
        if user_exists and title :
            task_check = session.run("MATCH (c:Task {title: $title}) RETURN c", title=title)
            task_exists = [record.data() for record in task_check]
            if not task_exists:
                session.run("CREATE (t:Task {title: $title}) RETURN t", title=title)
                session.run(
                    """
                    MATCH (u:Task {title: $username}), (t:Task {title: $title})
                    MERGE (u)-[:ASSIGNED_TO]->(t)
                    """,
                    username=user,
                    title=title
                )
                return{
                    'message': 'The child task was created and data loaded in Neo4j',
                    'status': '200'
                }
            else:
                return {"label is already there"}
            
        
        user_result = session.run("MATCH (u:User {username: $username}) RETURN u", username=user)
        user_records = [record.data() for record in user_result]
        print(user_records)

        if user_records and title:
            # Check if the child task already exists
            task_check = session.run("MATCH (c:Task {title: $title}) RETURN c", title=title)
            task_exists = [record.data() for record in task_check]

            # If the child task does not exist, create it and link to the parent task or user
            if not task_exists:
                session.run(
                    """
                    MATCH (p:User {username: $parentname})
                    CREATE (s:Task {title: $title})
                    MERGE (p)-[:Sub_Assign]->(s)
                    RETURN s
                    """,
                    parentname=user,
                    title=title
                )
                return{"label is created and assigned"}
            else :
                return{"label is already there ."}
            

