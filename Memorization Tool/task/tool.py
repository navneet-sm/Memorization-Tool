from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Flashcards(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
wait_ = 0
query = session.query(Flashcards).all()


def main():
    global query
    x = ''
    while x != '3':
        x = input("1. Add flashcards\n2. Practice flashcards\n3. Exit\n")
        if x == '1':
            flashcard_menu()
        elif x == '2':
            if len(session.query(Flashcards).all()) == 0:
                print('There is no flashcard to practice!')
            else:
                practice_menu()
        elif x == '3':
            print('Bye!')
        else:
            print(f'{x} is not an option')
            pass


def flashcard_menu():
    card_id, q, a, y = 1, '', '', ''
    while y != '2':
        y = input("1. Add a new flashcard\n2. Exit\n")
        if y == '1':
            while len(q.strip()) == 0:
                q = input('Question:\n')
            while len(a.strip()) == 0:
                a = input('Answer:\n')
            add_flashcard = Flashcards(id=card_id, question=q, answer=a, box_number=1)
            session.add(add_flashcard)
            session.commit()
            q, a = '', ''
            card_id += 1
        elif y == '2':
            pass
        else:
            print(f'{y} is not an option')


def practice_menu():
    data = session.query(Flashcards).all()
    i = 0
    while i < (len(data)):
        print(f'Question: {data[i].question}')
        z = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n')
        if z == 'y':
            print(f'Answer: {data[i].answer}\n')
            learning_menu(i)
        elif z == 'n':
            learning_menu(i)
        elif z == 'u':
            update_menu(i)
        else:
            print(f'{z} is not an option')
            practice_menu()
        i += 1


def update_menu(i):
    data = session.query(Flashcards).all()
    new_q, new_a = '', ''
    z1 = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n')
    try:
        card_id = session.query(Flashcards).all()[i].id
    except IndexError:
        card_id = session.query(Flashcards).all()[i - 1].id
        i -= 1
    if z1 == 'd':
        session.delete(session.query(Flashcards).all()[i])
        session.commit()
        return 'delete'
    elif z1 == 'e':
        while len(new_q.strip()) == 0:
            new_q = input(f'current question: {data[i].question}\n'
                          f'please write a new question: \n')
            session.query(Flashcards).filter(Flashcards.id == card_id).update({Flashcards.question: new_q})
        while len(new_a.strip()) == 0:
            new_a = input(f'current answer: {data[i].answer}\n'
                          f'please write a new answer: \n')
            session.query(Flashcards).filter(Flashcards.id == card_id).update({Flashcards.answer: new_a})
    else:
        print(f'{z1} is not an option')
    session.commit()


def learning_menu(i):
    data = session.query(Flashcards).all()
    global wait_
    card_id = session.query(Flashcards).all()[i].id
    z2 = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
    if z2 == 'y':
        if data[i].box_number != 3:
            session.query(Flashcards).filter(Flashcards.id == card_id).update(
                {Flashcards.box_number: Flashcards.box_number + 1})
        if data[i].box_number == 3:
            wait_ += 1
            if wait_ == 2:
                delete_box = session.query(Flashcards).filter(Flashcards.box_number == 3).all()
                for item in delete_box:
                    session.delete(item)
                session.commit()
                wait_ = 0

    elif z2 == 'n':
        if data[i].box_number != 1:
            session.query(Flashcards).filter(Flashcards.id == card_id).update(
                {Flashcards.box_number: 1})
    else:
        print(f'{z2} is not an option')
    session.commit()


main()
