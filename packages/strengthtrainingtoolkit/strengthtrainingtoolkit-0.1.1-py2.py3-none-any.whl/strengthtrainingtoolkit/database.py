from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import logging
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

Base = declarative_base()


trainer_table = Table("trainer_association", Base.metadata,
                      Column("trainer_id", Integer, ForeignKey("trainers.id")),
                      Column("athlete_id", Integer, ForeignKey("users.id"))
                      )

muscle_group_table = Table("musclegroup_associaton", Base.metadata,
                           Column("plannedexercise_id", Integer, ForeignKey("exercise_descriptions.id")),
                           Column("musclegroup_id", Integer, ForeignKey("musclegroups.id"))
                           )
# TODO: think of data validation (marshmellow?)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    trainers = relationship(
        "Trainer",
        secondary=trainer_table,
        back_populates="athletes"
    )
    programs = relationship("Program", order_by="Program.id", back_populates="user")
    
    def __repr__(self):
        return "<User(name={})>".format(self.name)


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", uselist=False)

    athletes = relationship(
        "User",
        secondary=trainer_table,
        back_populates="trainers"
    )

    def __repr__(self):
        return "<Trainer(user={})>".format(self.user.name)


class SchemaExerciseOrder(Base):
    __tablename__ = "schema_exercise_order"

    trainingsschema_id = Column(Integer, ForeignKey("trainingsschemas.id"), primary_key=True)
    exercise_description_id = Column(Integer, ForeignKey("exercise_descriptions.id"), primary_key=True)
    identifier = Column(String)

    trainingsschema = relationship("TrainingsSchema", back_populates="schema_exercise_orders")
    exercise_description = relationship("ExerciseDescription", back_populates="schema_exercise_orders")


class MuscleGroup(Base):
    __tablename__ = "musclegroups"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    primary_muscle_exercises = relationship("ExerciseDescription",
                                            secondary=muscle_group_table,
                                            back_populates="primary_muscle_group")
    secondary_muscle_exercises = relationship("ExerciseDescription",
                                              secondary=muscle_group_table,
                                              back_populates="secondary_muscle_group")

    def __repr__(self):
        return "<MuscleGroup(name={})>".format(self.name)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    exercise_descriptions = relationship("ExerciseDescription", back_populates="equipment")

    def __repr__(self):
        return "<Equipment(name={})>".format(self.name)


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    conversion_factor = Column(Float)

    def __repr__(self):
        return "<Metric(name='{}')>".format(self.name)


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    comment = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="programs")

    trainingsschemas = relationship("TrainingsSchema", order_by="TrainingsSchema.id", back_populates="program")
    iterations = relationship("Iteration", order_by="Iteration.number", back_populates="program")

    def __repr__(self):
        return "<Program(name='{}')>".format(self.name)


class TrainingsSchema(Base):
    __tablename__ = "trainingsschemas"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    comment = Column(String)

    program_id = Column(Integer, ForeignKey("programs.id"))
    program = relationship("Program", back_populates="trainingsschemas")

    iterations = relationship("Iteration", back_populates="trainingsschema")

    schema_exercise_orders = relationship("SchemaExerciseOrder",  back_populates="trainingsschema")

    planned_workouts = relationship("PlannedWorkout", order_by="PlannedWorkout.id", back_populates="trainingsschema")

    # THINKOF way to list/show order of exercises (present in SchemaExerciseOrder.identifier)
    # THINKOF --> this becomes easier! for now fixed by returning a dict for exercise_descriptions
    @property  # THINKOF: need of a set property?
    def exercise_descriptions(self):
        return {seo.identifier: seo.exercise_description for seo in self.schema_exercise_orders}

    def __repr__(self):
        return "<TrainingsSchema(name='{}')>".format(self.name)


class Iteration(Base):  # or class Week(Base)?
    __tablename__ = "iterations"

    program_id = Column(Integer, ForeignKey("programs.id"), primary_key=True)
    trainingsschema_id = Column(Integer, ForeignKey("trainingsschemas.id"), primary_key=True)
    planned_workout_id = Column(Integer, ForeignKey("planned_workouts.id"), primary_key=True)

    name = Column(String)
    number = Column(Integer)

    program = relationship("Program", back_populates="iterations")
    trainingsschema = relationship("TrainingsSchema", back_populates="iterations")
    planned_workout = relationship("PlannedWorkout", back_populates="iteration")

    def __repr__(self):
        return "<Iteration(name={})>".format(self.name)


class PlannedWorkout(Base):
    __tablename__ = "planned_workouts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime)
    comment = Column(String)

    trainingsschema_id = Column(Integer, ForeignKey("trainingsschemas.id"))
    trainingsschema = relationship("TrainingsSchema", back_populates="planned_workouts")

    iteration = relationship("Iteration", back_populates="planned_workout")

    planned_exercises = relationship("PlannedExercise", order_by="PlannedExercise.id", back_populates="planned_workout")

    workout = relationship("Workout", back_populates="plannedworkout")

    def __repr__(self):
        return "<PlannedWorkout(name={})>".format(self.name)


class ExerciseDescription(Base):
    __tablename__ = "exercise_descriptions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    rest = Column(Integer)
    speed_pattern = Column(String)  # THINKOF 1) better name 2) combined exercises -->
    #  THINKOF (no concentric-isometric-eccentric-isometric scheme but longer)
    primary_muscle_group = relationship("MuscleGroup",
                                        secondary=muscle_group_table,
                                        back_populates="primary_muscle_exercises")
    secondary_muscle_group = relationship("MuscleGroup",
                                          secondary=muscle_group_table,
                                          back_populates="secondary_muscle_exercises")

    schema_exercise_orders = relationship("SchemaExerciseOrder", back_populates="exercise_description")

    equipment_id = Column(Integer, ForeignKey("equipment.id"))                  
    equipment = relationship("Equipment", back_populates="exercise_descriptions")
    comment = Column(String)

    @property
    def trainingsschemas(self):  # THINKOF: need of a set property?
        return [seo.trainingsschema for seo in self.schema_exercise_orders]

    def __repr__(self):
        return "<ExerciseDescription(name={})>".format(self.name)


class PlannedExercise(Base):
    # THINKOF: it's possible to create a PlannedExercise without name or link to ExerciseDescription
    __tablename__ = "planned_exercises"
    _mapper_args__ = {
        'exclude_properties': ["_regex_template"]
    }

    _regex_template = "(\d+) ?[xX*] ?(\d+\.?\d+)(\w+)"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    exercisedescription_id = Column(Integer, ForeignKey("exercise_descriptions.id"))
    exercise_description = relationship("ExerciseDescription")

    planned_workout_id = Column(Integer, ForeignKey("planned_workouts.id"))
    planned_workout = relationship("PlannedWorkout", back_populates="planned_exercises")

    planned_loads = relationship("PlannedLoad", order_by="PlannedLoad.id", back_populates="plannedexercise")

    exercise = relationship("Exercise", order_by="Exercise.id", back_populates="plannedexercise")

    @property
    def sets(self):
        return ", ".join([str(l) for l in self.planned_loads])

    @sets.setter
    def sets(self, value):  # TODO: this should be data validated!

        self.planned_loads = [Load(repetitions=int(m.group(1)), resistance=float(m.group(2)), metric=m.group(3))
                              for m in re.finditer(self._regex_template, value)]

    def __repr__(self):
        name = self.name or self.exercise_description.name
        return "<PlannedExercise(name={})>".format(name)


class PlannedLoad(Base):
    __tablename__ = "planned_loads"
    _mapper_args__ = {
        'exclude_properties': ['_str_template']
    }
    id = Column(Integer, primary_key=True)
    repetitions = Column(Integer)
    resistance = Column(Float)
    metric = Column(String)

    plannedexercise_id = Column(Integer, ForeignKey("planned_exercises.id"))
    plannedexercise = relationship("PlannedExercise", back_populates="planned_loads")

    _str_template = "{repetitions} x {resistance}{metric}"
    _regex_template = "(\d+) ?[xX*] ?(\d+\.?\d+)(\w+)"

    @classmethod
    def regex(cls, value):
        repetitions, resistance, metric = re.search(cls._regex_template, value).groups()
        return cls(repetitions=int(repetitions), resistance=float(resistance), metric=metric)

    # aliases
    @property
    def reps(self):
        return self.repetitions

    @reps.setter
    def reps(self, value):
        self.repetitions = value

    @property
    def load(self):
        return self.resistance

    @load.setter
    def load(self, value):
        self.resistance = value

    @property
    def unit(self):
        return self.metric

    @unit.setter
    def unit(self, value):
        self.metric = value

    def __repr__(self):
        return "<PlannedLoad(repetitions={}, resistance={:.02f}, metric={})>".\
            format(self.repetitions, self.resistance, self.metric)

    def __str__(self):
        return self._str_template.format(repetitions=self.repetitions, resistance=self.resistance, metric=self.metric)


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime)
    rpe = Column(Float)
    comment = Column(String)
    plannedworkout_id = Column(Integer, ForeignKey("planned_workouts.id"))
    plannedworkout = relationship("PlannedWorkout", back_populates="workout")

    exercises = relationship("Exercise", order_by="Exercise.id", back_populates="workout")

    def __repr__(self):
        return "<Workout(name={})>".format(self.name)


class Exercise(Base):
    __tablename__ = "exercises"
    _mapper_args__ = {
        'exclude_properties': ["_regex_template"]
    }
    id = Column(Integer, primary_key=True)
    name = Column(String)

    workout_id = Column(Integer, ForeignKey("workouts.id"))
    workout = relationship("Workout", back_populates="exercises")

    plannedexercise_id = Column(Integer, ForeignKey("planned_exercises.id"))
    plannedexercise = relationship("PlannedExercise", back_populates="exercise")

    loads = relationship("Load", order_by="Load.id", back_populates="exercise")

    _regex_template = "(\d+) ?[xX*] ?(\d+\.?\d+)(\w+)"

    @property
    def sets(self):
        return ", ".join([str(l) for l in self.loads])

    @sets.setter
    def sets(self, value):  # TODO: this should be data validated!

        self.loads = [Load(repetitions=int(m.group(1)), resistance=float(m.group(2)), metric=m.group(3))
                      for m in re.finditer(self._regex_template, value)]

    def __repr__(self):
        return "<Exercise(name={})>".format(self.name)


class Load(Base):
    __tablename__ = "loads"
    _mapper_args__ = {
        'exclude_properties': ['_str_template']
    }
    id = Column(Integer, primary_key=True)
    repetitions = Column(Integer)
    resistance = Column(Float)
    metric = Column(String)

    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="loads")

    _str_template = "{repetitions} x {resistance}{metric}"

    # aliases
    @property
    def reps(self):
        return self.repetitions

    @reps.setter
    def reps(self, value):
        self.repetitions = value

    @property
    def load(self):
        return self.resistance

    @load.setter
    def load(self, value):
        self.resistance = value

    @property
    def unit(self):
        return self.metric

    @unit.setter
    def unit(self, value):
        self.metric = value

    def __repr__(self):
        return "<Load(repetitions={}, resistance={:.02}, metric={})>".format(self.repetitions, self.resistance, self.metric)

    def __str__(self):
        return self._str_template.format(repetitions=self.repetitions, resistance=self.resistance, metric=self.metric)


if __name__ == "__main__":
    pass
