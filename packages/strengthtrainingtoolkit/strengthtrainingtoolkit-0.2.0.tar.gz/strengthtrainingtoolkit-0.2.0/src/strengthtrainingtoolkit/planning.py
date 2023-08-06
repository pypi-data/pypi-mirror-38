import streprogen
import re
import itertools
from .database import Program, TrainingsSchema, ExerciseDescription,\
    Iteration, PlannedWorkout, PlannedExercise, PlannedLoad, SchemaExerciseOrder
from sqlalchemy.orm.exc import NoResultFound


def program_to_sql(program, session=None):
    """

    :param program:
    :return:
    """
    if not isinstance(program, streprogen.Program):
        raise TypeError(f"program '{program}' is not a streprogen.Program object!")

    if not program._rendered:
        raise ValueError(f"program '{program}' is not rendered, can't extract data!")

    # create a Program sqlalchemy object
    program_ = Program(name=program.name)

    # create a TrainingsSchema (based on streprogen.Day) object for each schema
    program_.trainingsschemas = [
        TrainingsSchema(name=day.name) for day in program.days
    ]

    # create ExerciseDescription for each exercise in each trainingsschema
    seos = []
    for day, schema in zip(program.days, program_.trainingsschemas):
        exercise_descriptions_ = []
        for ex_num, exercise in enumerate(itertools.chain(day.dynamic_exercises, day.static_exercises)):
            # TODO: get from database if exists, else create new (as is done below)
            # import pdb; pdb.set_trace()  # FINDOUT: if session can't find anything, does it return None?
            # FINDOUT --> that is what I assumed here
            exercise_description_ = None
            if session:
                try:
                    exercise_description_ = session.query(ExerciseDescription).filter_by(name=exercise.name).one()
                except NoResultFound:
                    exercise_description_ = None

            if not exercise_description_:
                exercise_description_ = ExerciseDescription(name=exercise.name)
            seo = SchemaExerciseOrder(trainingsschema=schema, exercise_description=exercise_description_,
                                      identifier=f"{ex_num}")
            seos.append(seo)

    # for each Iteration (week), and TrainingsSchema (day), create a PlannedWorkout object
    # and create an Iteration object linking Project, TrainingsSchema, &
    # PlannedWorkout objects
    for _week, _workouts in program._rendered.items():

        # create a PlannedExercise for eac in each PlannedWorkout
        for schema_, (_workout, _exercises) in zip(program_.trainingsschemas, _workouts.items()):
            workout_ = PlannedWorkout(name=_workout.name, trainingsschema=schema_)
            iteration_ = Iteration(program=program_, name="week", number=_week, planned_workout=workout_)
            program_.iterations.append(iteration_)
            for exdesc, (_exercise, _loads) in zip(schema_.exercise_descriptions, _exercises.items()):
                exercise_ = PlannedExercise(exercise_description=exdesc, planned_workout=workout_)
                for _load in _loads['strings']:
                    load_ = PlannedLoad.regex(_load)
                    exercise_.planned_loads.append(load_)

    return program_


