from strengthtrainingtoolkit.database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime as dt


def create_memory_session():
    engine = create_engine("sqlite:///:memory:", echo=True)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def test_load():
    session = create_memory_session()

    l = Load(reps=5, load=100, unit="kg")  # we're able to use aliased properties! whooooo
    session.add(l)
    session.commit()
    l_ = session.query(Load).one()
    return session, l_


def test_exercise():
    session = create_memory_session()

    e = Exercise(name="bench press")
    e.loads = [
        Load(repetitions=5, resistance=100, metric="kg"),
        Load(repetitions=5, resistance=100, metric="kg"),
        Load(repetitions=5, resistance=100, metric="kg")
    ]

    session.add(e)
    session.commit()
    e_ = session.query(Exercise).one()
    l_ = session.query(Load).all()
    return session, e_, l_


def test_workout():
    session = create_memory_session()

    w = Workout(name="Workout 1", datetime=dt.datetime.now())
    e1 = Exercise(name="bench press")
    e1.loads = [Load(repetitions=5, resistance=100, metric="kg")] * 3
    e2 = Exercise(name="squat")
    e2.loads = [Load(repetitions=5, resistance=150, metric="kg")] * 3
    w.exercises = [e1, e2]

    session.add(w)
    session.commit()
    w_ = session.query(Workout).one()
    e_ = session.query(Exercise).all()
    l_ = session.query(Load).all()

    return session, w_, e_, l_


def test_planned_load():
    session = create_memory_session()

    l = PlannedLoad(reps=5, load=100, unit="kg")  # we're able to use aliased properties! whooooo
    session.add(l)
    session.commit()
    l_ = session.query(PlannedLoad).one()
    return session, l_


def test_planned_exercise():
    session = create_memory_session()

    e = PlannedExercise()
    e.planned_loads = [
        PlannedLoad(repetitions=5, resistance=100, metric="kg"),
        PlannedLoad(repetitions=5, resistance=100, metric="kg"),
        PlannedLoad(repetitions=5, resistance=100, metric="kg")
    ]

    session.add(e)
    session.commit()
    e_ = session.query(PlannedExercise).one()
    l_ = session.query(PlannedLoad).all()
    return session, e_, l_


def test_planned_workout():
    session = create_memory_session()

    w = PlannedWorkout(name="Workout 1")
    e1 = PlannedExercise()
    e1.planned_loads = [PlannedLoad(repetitions=5, resistance=100, metric="kg")] * 3
    e2 = PlannedExercise()
    e2.planned_loads = [PlannedLoad(repetitions=5, resistance=150, metric="kg")] * 3
    w.planned_exercises = [e1, e2]

    session.add(w)
    session.commit()
    w_ = session.query(PlannedWorkout).one()
    e_ = session.query(PlannedExercise).all()
    l_ = session.query(PlannedLoad).all()
    return session, w_, e_, l_


def test_musclegroup():
    session = create_memory_session()

    mg = MuscleGroup(name="Biceps")

    session.add(mg)
    session.commit()

    mg_ = session.query(MuscleGroup).one()

    return session, mg_


def test_equipment():
    session = create_memory_session()

    e = Equipment(name="barbell")

    session.add(e)
    session.commit()

    e_ = session.query(Equipment).one()
    return session, e_


def test_user():
    session = create_memory_session()

    u = User(name="Timo")

    session.add(u)
    session.commit()

    u_ = session.query(User).one()
    return session, u_


def test_user_trainer():
    session = create_memory_session()

    u1 = User(name="Timo")
    u2 = User(name="Bram")
    t = Trainer(user=u2)
    t.athletes = [u1]

    session.add(t)
    session.commit()

    u_ = session.query(User).all()
    t_ = session.query(Trainer).one()

    return session, u_, t_


def test_program():
    session = create_memory_session()

    p = Program(name="My first program!")
    session.add(p)
    session.commit()

    p_ = session.query(Program).one()

    return session, p_


def test_user_program():
    session = create_memory_session()

    u = User(name="Timo")
    t = Trainer(user=u)
    u.trainers = [t]
    p = Program(name="My first program!", user=u)

    session.add(p)
    session.commit()

    u_ = session.query(User).one()
    t_ = session.query(Trainer).one()
    p_ = session.query(Program).one()

    return session, u_, t_, p_


def test_trainingsschema():
    session = create_memory_session()

    p = Program(name="My first program containing schemas!")
    p.trainingsschemas = [
        TrainingsSchema(name="day 1"),
        TrainingsSchema(name="day 2")
    ]

    session.add(p)
    session.commit()

    p_ = session.query(Program).one()
    ts_ = session.query(TrainingsSchema).all()
    return session, p_, ts_


def test_exercise_description():
    session = create_memory_session()

    ed = ExerciseDescription(name="bench press")

    session.add(ed)
    session.commit()

    ed_ = session.query(ExerciseDescription).one()

    return session, ed_


def test_trainingsschema_exercise_description():
    session = create_memory_session()

    u = User(name="Timo")
    t = Trainer(user=u)

    u.trainers = [t]

    ed1 = ExerciseDescription(name="bench press")
    ed2 = ExerciseDescription(name="squat")
    ed3 = ExerciseDescription(name="deadlift")
    ed4 = ExerciseDescription(name="pull-up")

    ts1 = TrainingsSchema(name="day 1")
    ts2 = TrainingsSchema(name="day 2")

    seo1 = SchemaExerciseOrder(trainingsschema=ts1, exercise_description=ed1, identifier="A1")
    seo2 = SchemaExerciseOrder(trainingsschema=ts1, exercise_description=ed2, identifier="A2")
    seo3 = SchemaExerciseOrder(trainingsschema=ts2, exercise_description=ed3, identifier="A1")
    seo4 = SchemaExerciseOrder(trainingsschema=ts2, exercise_description=ed4, identifier="A2")

    p = Program(name="My first program!", user=u)

    p.trainingsschemas = [ts1, ts2]

    session.add(p)
    session.commit()

    u_ = session.query(User).one()
    t_ = session.query(Trainer).one()
    p_ = session.query(Program).one()
    seo_ = session.query(SchemaExerciseOrder).all()
    ed_ = session.query(ExerciseDescription).all()
    ts_ = session.query(TrainingsSchema).all()

    return session, u_, t_, p_, seo_, ed_, ts_


def test_trainingsschema_iteration():
    session = create_memory_session()

    u = User(name="Timo")
    t = Trainer(user=u)

    u.trainers = [t]

    ed1 = ExerciseDescription(name="bench press")
    ed2 = ExerciseDescription(name="squat")
    ed3 = ExerciseDescription(name="deadlift")
    ed4 = ExerciseDescription(name="pull-up")

    ts1 = TrainingsSchema(name="day 1")
    ts2 = TrainingsSchema(name="day 2")

    seo1 = SchemaExerciseOrder(trainingsschema=ts1, exercise_description=ed1, identifier="A1")
    seo2 = SchemaExerciseOrder(trainingsschema=ts1, exercise_description=ed2, identifier="A2")
    seo3 = SchemaExerciseOrder(trainingsschema=ts2, exercise_description=ed3, identifier="A1")
    seo4 = SchemaExerciseOrder(trainingsschema=ts2, exercise_description=ed4, identifier="A2")

    p = Program(name="My first program!", user=u)

    p.trainingsschemas = [ts1, ts2]

    for schema in p.trainingsschemas:
        for week in range(1, 5): #4 weeks total
            workout = PlannedWorkout(trainingsschema=schema)
            iteration = Iteration(program=p, trainingsschema=schema, planned_workout=workout)
            p.iterations.append(iteration)

    session.add(p)
    session.commit()

    u_ = session.query(User).one()
    t_ = session.query(Trainer).one()
    p_ = session.query(Program).one()
    seo_ = session.query(SchemaExerciseOrder).all()
    ed_ = session.query(ExerciseDescription).all()
    ts_ = session.query(TrainingsSchema).all()
    i_ = session.query(Iteration).all()
    pw_ = session.query(PlannedWorkout).all()

    return session, u_, t_, p_, seo_, ed_, ts_, i_, pw_


p = Program(name="my program", comment="none")


maandag = PlannedWorkout(name="maandag")
dinsdag = PlannedWorkout(name="dinsdag")

squatrack = Equipment(name="squat rack")
bpress_equipment = Equipment(name="bench press")
barbell = Equipment(name="barbell")

quads = MuscleGroup(name="suadriceps")
hams = MuscleGroup(name="hamstrings")
chest = MuscleGroup(name="chest")
triceps = MuscleGroup(name="triceps")

bench_press = ExerciseDescription(
    name="bench press",
    description="This is a benchpress",
    rest=60,
    primary_muscle_group=[quads],
    secondary_muscle_group=[triceps],
    equipment=bpress_equipment,
    comment="")

press_loads = [PlannedLoad(repetitions=5, resistance=100, metric="kg"),
               PlannedLoad(repetitions=5, resistance=100, metric="kg")]
bpress = PlannedExercise(exercise_description=bench_press,
                         planned_loads=press_loads)

maandag.planned_exercises = [bpress]
