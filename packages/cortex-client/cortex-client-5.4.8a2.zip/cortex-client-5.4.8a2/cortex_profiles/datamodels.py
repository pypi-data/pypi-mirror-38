from typing import NamedTuple, Optional, List, Union, Tuple

from . import schemas
from .utils import merge_dicts


FindQuery = dict
AggregateQuery = List[dict]
OrderedList = List


class LatestCommitPointer(NamedTuple):
    id: str  # What is the id of this piece of data?
    commitId: str  # What commit does this pointer point to?
    profileId: str  # Who is this pointer for?
    environmentId: str  # What environment is this pointer in?
    tenantId: str  # What tenant is this pointer in?
    createdAt: str  # When was this pointer created?
    context: str = schemas.CONTEXTS.SESSION  # What is the type of the data being captured by this data type?
    version: str = schemas.CONTEXTS.VERSION  # What version of the data type is being adhered to?


class CortexProperties(NamedTuple):
    jwt_token:str
    api_endpoint:str="https://api.cortex.insights.ai"
    environmentId:str="cortex/default"


class Link(NamedTuple):
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    title: Optional[str] = None # What is the human friendly name of this link?
    version: str = schemas.CONTEXTS.VERSION  # What version of the data type is being adhered to?


class UserActivity(NamedTuple):
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    profileId: str # What profile initiated the activity?
    appId: str # Which app did this activity occur on?
    isoUTCStartTime: str # When did this activity start?
    isoUTCEndTime: str # When did this activity end?


class Session(NamedTuple):
    id: str  # What is the id of this piece of data?
    profileId: str  # What profile initiated the activity?
    appId: str  # Which app did this activity occur on?
    isoUTCStartTime: str  # When did this activity start?
    isoUTCEndTime: str  # When did this activity end?
    durationInSeconds: float # How long did the session last?
    context: str = schemas.CONTEXTS.SESSION  # What is the type of the data being captured by this data type?
    version: str = schemas.CONTEXTS.VERSION  # What version of the data type is being adhered to?


class InsightTag(NamedTuple):
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    insight: Link # What insight is this tag about?
    concept: Link # What concept is being tagged by the insight?
    relationship: Link # What relationship does the tagged concept have with regards to the insight?
        # What are all the different concept relationships that can be tagged in an insight?
            # Is the insight about the concept?
            # Is the insight related to the insight?
            # Does the insight <predict> the concept?
            # Does the insight <simulate> the concept?


class Insight(NamedTuple):
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    insightType: str # What kind of insight is this?
    profileId: str # What profile was this insight generated for?
    dateGeneratedUTCISO: str # When was this insight generated?
    appId: str # Which app was this insight generated for?
    tags: List # What concepts were tagged in this insight?


# - [x] The number of times a concept is related to an insight that currently in the liked state vs that ever was in the liked state ...

class InsightInteractionEvent(NamedTuple):
    id: str  # What is the id of this piece of data?
    sessionId:str # What session did the interaction occur in?
    profileId: str  # Which profile was responsible for this interaction?
    insightId:str # Which insight's was interacted on?
    interactionType:str # What type of interaction was performed on the insight? TODO ... what is the list of interaction types?
    interactionDateISOUTC:str # When did the insight transition to this state?
    properties: dict # What additional information is needed when transitioning into a specific state?
    custom:Optional[dict] # Is there any use case specific stuff we need to know about the interaction?
    version: str = schemas.CONTEXTS.VERSION  # What version of the data type is being adhered to?
    context: str = schemas.CONTEXTS.INSIGHT_INTERACTION  # What is the type of the data being captured by this data type?


class InsightRelatedToConceptTag(NamedTuple):
    """
    Representing how an insight relates to other concepts ...
    """
    version: str  # What version of the data type is being adhered to?
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    insight: Link # What insight is this relationship about?
    concept: Link # What concept is the insight related to?


# Class InsightPresented
#     sessionId: str # Which session was this insight presented to the user in?
#     insightId: str # Which insight was presented to the end user?
# ---------------------------------------------------------------------------------


class ProfileLock(NamedTuple):
    lockerId: str # Who locked the profile?
    profileId: str # What profile is locked?
    locked: str # When was the profile locked?
    ttl: int # How many seconds will the lock last for before breaking?
    lockedUntil: str # Until when will this profile remain locked if not already unlocked?
    unlocked: Optional[str] # When was the profile unlocked?
    isLocked: bool # Is the profile still locked?


# ---------------------------------------------------------------------------------


# How do I say this extends profile attribute ...
    # print(SESSIONS_COLS._fields) -> ('CONTEXT', 'ID', 'ISOUTCENDTIME', 'ISOUTCSTARTTIME', 'PROFILEID', 'APPID', 'DURATIONINSECONDS')
    # print(SESSIONS_COLS._field_types) -> OrderedDict([('CONTEXT', <class 'str'>), ('ID', <class 'str'>), ('ISOUTCENDTIME', <class 'str'>), ('ISOUTCSTARTTIME', <class 'str'>), ('PROFILEID', <class 'str'>), ('APPID', <class 'str'>), ('DURATIONINSECONDS', <class 'str'>)])


class InferredProfileAttribute(NamedTuple):
    id: str  # What is the id of this piece of data?
    profileId: str  # Who is this attribute applicable to?
    createdAt: str  # When was this attribute created?
    inferredAt: str # When was this attribute inferred at?
    attributeKey: str  # What is the id of the attribute?
    attributeValue: object  # What value is associated with the profile attribute?
    profileType: str = schemas.CONTEXTS.END_USER_PROFILE  # What kind of entity is represented by this profile?
    onLatestProfile: bool = True  # Is this attribute on the latest profile?
    tenantId: str = None
    environmentId: str = None
    inferred: bool = True  # Was this attribute inferred?
    commits: List[str] = []  # What commits is this attribute associated with?
    context: str = schemas.CONTEXTS.INFERRED_PROFILE_ATTRIBUTE  # What is the type of the data being captured by this data type?
    version: str = schemas.CONTEXTS.VERSION  # What version of the data type is being adhered to?


class ObservedProfileAttribute(NamedTuple):
    # How do I say this extends profile attribute ...
    id: str  # What is the id of this piece of data?
    profileId: str # Who is this attribute applicable to?
    createdAt: str  # When was this attribute created?
    observedAt: str # When was this attribute observed at?
    attributeKey: str # What is the id of the attribute?
    attributeValue: object  # What value is associated with the profile attribute?
    profileType: str = schemas.CONTEXTS.END_USER_PROFILE  # What kind of entity is represented by this profile?
    onLatestProfile: bool = True  # Is this attribute on the latest profile?
    tenantId: str = None
    environmentId: str = None
    observed: bool = True  # Was this attribute observed?
    commits: List[str] = []  # What commits is this attribute associated with?
    context: str = schemas.CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE  # What is the type of the data being captured by this data type?
    version: str = schemas.CONTEXTS.VERSION # What version of the data type is being adhered to?


class DeclaredProfileAttribute(NamedTuple):
    # How do I say this extends profile attribute ...
    id: str  # What is the id of this piece of data?
    profileId: str # Who is this attribute applicable to?
    createdAt: str  # When was this attribute created?
    declaredAt: str # When did the user declare this attribute about themselves?
    attributeKey: str # What is the id of the attribute?
    attributeValue: object  # What value is associated with the profile attribute?
    profileType: str = schemas.CONTEXTS.END_USER_PROFILE  # What kind of entity is represented by this profile?
    onLatestProfile: bool = True  # Is this attribute on the latest profile?
    tenantId : str = None
    environmentId: str = None
    declared: bool = True  # Was this profile attribute declared by the user?
    commits: List[str] = []  # What commits is this attribute associated with?
    context: str = schemas.CONTEXTS.DECLARED_PROFILE_ATTRIBUTE  # What is the type of the data being captured by this data type?
    version: str = schemas.CONTEXTS.VERSION # What version of the data type is being adhered to?


ProfileAttribute = Union[InferredProfileAttribute, DeclaredProfileAttribute, ObservedProfileAttribute]


def load_profile_attribute_from_dict(d: dict) -> ProfileAttribute:
    if d.get("context") == schemas.CONTEXTS.INFERRED_PROFILE_ATTRIBUTE:
        return InferredProfileAttribute(**d)
    if d.get("context") == schemas.CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE:
        return ObservedProfileAttribute(**d)
    if d.get("context") == schemas.CONTEXTS.DECLARED_PROFILE_ATTRIBUTE:
        return DeclaredProfileAttribute(**d)
    return None


# class DimensionalAttribute(NamedTuple):
#     # How do I say this extends profile attribute ...
#     id: str  # What is the id of this piece of data?
#     attributeKey: str # What is the id of the attribute?
#     profileId: str # Who is this attribute applicable to?
#     createdAt: str  # When was this attribute created?
#     dimensionContext: str  # What version of the data type is being adhered to?
#     valueContext: str  # What is the type of the data being captured by this data type?
#     dimensions: List[Dimension] # What information does this attribute contain?
#     context: str = schemas.CONTEXTS.DIMENSIONAL_PROFILE_ATTRIBUTE# What is the type of the data being captured by this data type?
#     version: str = schemas.CONTEXTS.VERSION # What version of the data type is being adhered to?
#
#
# class CounterAttribute(NamedTuple):
#     # - [ ] TODO How do I say this extends profile attribute ...
#     id: str  # What is the id of this piece of data?
#     attributeKey: str # What is the id of the attribute?
#     profileId: str # Who is this attribute applicable to?
#     createdAt: str  # When was this attribute created?
#     value: int # What information does this attribute contain?
#     context: str = schemas.CONTEXTS.NUMERICAL_PROFILE_ATTRIBUTE # What is the type of the data being captured by this data type?
#     version: str = schemas.CONTEXTS.VERSION # What version of the data type is being adhered to?
#

class ObjectValue(NamedTuple):
    value: object
    context:str = schemas.CONTEXTS.OBJECT_PROFILE_ATTRIBUTE_VALUE
    version:str = schemas.CONTEXTS.VERSION


class RelationshipValue(NamedTuple):
    """
    Representing the content of a percentage attribute ...
    """
    relationshipId : str
    relatedConceptId : str
    relationshipProperties: dict = {}
    context:str = schemas.CONTEXTS.RELATIONSHIP_PROFILE_ATTRIBUTE_VALUE
    version:str = schemas.CONTEXTS.VERSION

class PercentileAttributeValue(NamedTuple):
    """
    Representing the content of a percentage attribute ...
    """
    value: float
    context:str = schemas.CONTEXTS.PERCENTILE_PROFILE_ATTRIBUTE_VALUE
    version:str = schemas.CONTEXTS.VERSION


class AverageAttributeValue(NamedTuple):
    """
    Representing the content of a percentage attribute ...
    """
    value: float
    context: str = schemas.CONTEXTS.AVERAGE_PROFILE_ATTRIBUTE_VALUE
    version: str = schemas.CONTEXTS.VERSION


class CounterAttributeContent(NamedTuple):
    """
    Representing the content of a counter attribute ...
    """
    value: int
    context: str = schemas.CONTEXTS.COUNTER_PROFILE_ATTRIBUTE_VALUE
    version: str = schemas.CONTEXTS.VERSION


class TotalAttributeContent(NamedTuple):
    """
    Representing the content of a counter attribute ...
    """
    value: float
    context: str = schemas.CONTEXTS.TOTAL_PROFILE_ATTRIBUTE_VALUE
    version: str = schemas.CONTEXTS.VERSION


class Dimension(NamedTuple):
    dimensionId: str
    dimensionValue: object
    # - [ ] Do we put versions on everything ... even it its meant to be nested? or only stuff saved in db?


class DimensionalAttributeContent(NamedTuple):
    value: List[Dimension]
    contextOfDimension: str  # What type is the dimension
    contextOfDimensionValue: str  # What type is the value associated with the dimension?
    context: str = schemas.CONTEXTS.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE
    version: str = schemas.CONTEXTS.VERSION


#
# ProfileAttributeKinds = Union[
#     PercentageAttributeContent,
#     CounterAttributeContent,
#     DimensionalAttributeContent,
#     MultiDimensionalAttributeContent
# ]


#
# class ProfileAttribute(NamedTuple):
#     """
#     Representing a profile attribute ...
#     These
#     # The profileId is more then a string ... its a resolvable string .. and when it gets resolved ... what should it return ...?
#     # The conceptId is more then a string ... its a resolvable string .. and when it gets resolved ... what should it return ...?
#     # The creation event tells us which "event" led to the creation of this attriubte ...
#     """
#     attributeId: str # What is the id of the attribute?
#     attributeType: str # What kind of attribute is this?
#     profileId: str # Who is this attribute applicable to?
#     conceptId: str # What concept is this attribute about?
#     createdAt: str # When was this attribute created?
#     meaning: str # What does the attribute mean?
#     content: ProfileAttributeKinds # What information does this attribute contain?


# class ProfileAttributeSummary(NamedTuple):
#     """
#     Representing a profile attribute ... that gets saved into the profile ...
#     attributeId: str # What is the id of the attribute?
#     Reason for omitting the following:
#         - attributeType: its assumed the profile structure contains information as to the different types of data within it ...
#     """
#     attributeId: str # What is the id of the attribute?
#     meaning: str # What does the attribute mean?
#     createdAt: str # When was this attribute created?
#     content: ProfileAttributeKinds # What information does this attribute contain?

# --------------------------------------------------------------------------------


# class ProfileSnapshot(NamedTuple):
#     snapshotId: str # What is the id of this snapshot
#     profileId: str # What profileId is represented by this snapshot ...
#     createdAt: str # When was this snapshot created?
#     content: Mapping[str, Any] # What is the actual content of the profile
#     commits: List[str] # What are all of the commit ids rolled into this snapshot ...


class ProfileAttributeMapping(NamedTuple):
    attributeKey: str # What is the name of the attribute in the profile?
    attributeId: str # What is the id for the attribute in the profile?


class Profile(NamedTuple):
    id: str  # What is the id of this piece of data? aka snapshotId
    createdAt: str # When was this snapshot created?
    tenantId: str # Which tenant does this attribute belong in?
    environmentId: str # Which environment does this profile live in?
    commitId: str  # Which commit is this linked based off of?
    version: str = schemas.CONTEXTS.VERSION  # What version of the system does this piece of data adhere to?
    context: str = schemas.CONTEXTS.PROFILE  # What is the type of the data being captured by this data type?
    attributes: List[ProfileAttributeMapping] = []  # Which attributes exist in this snapshot?

    @staticmethod
    def from_dict(d:dict):
        mapped_attributes = [] if not d.get("attributes") else d["attributes"]
        mapped_attributes = [
            ProfileAttributeMapping(**attr) if not isinstance(attr, ProfileAttributeMapping) else attr
            for attr in mapped_attributes
        ]
        return Profile(
            **merge_dicts(d, {
                "attributes": mapped_attributes
            })
        )


def get_types_of_union(union:Union) -> Tuple[type]:
    return union.__args__


class ProfileSnapshot(NamedTuple):
    id: str  # What is the id of this piece of data? aka snapshotId
    createdAt: str # When was this snapshot created?
    tenantId: str # Which tenant does this attribute belong in?
    environmentId: str # Which environment does this profile live in?
    commitId: str  # Which commit was responsible for creating this updated profile?
    version: str = schemas.CONTEXTS.VERSION  # What version of the system does this piece of data adhere to?
    context: str = schemas.CONTEXTS.PROFILE  # What is the type of the data being captured by this data type?
    attributes: List[ProfileAttribute] = []  # Which attributes exist in this snapshot?

    @staticmethod
    def from_dict(d:dict):
        mapped_attributes = [] if not d.get("attributes") else d["attributes"]
        mapped_attributes = [
            load_profile_attribute_from_dict(attr) if not isinstance(attr, get_types_of_union(ProfileAttribute)) else attr
            for attr in mapped_attributes
        ]
        return Profile(
            **merge_dicts(d, {
                "attributes": mapped_attributes
            })
        )


class ProfileCommit(NamedTuple):
    id: str  # What is the id of this piece of data? aka commitId
    createdAt: str  # When was this snapshot created?
    tenantId: str  # Which tenant does this attribute belong in?
    environmentId: str  # Which environment does this profile live in?
    profileId: str  # What profile is this commit on?
    extends: Optional[str] = None  # What is the id of the commit this commit extends?
    attributesModified: Optional[List[ProfileAttributeMapping]] = []  # Which attributes were modified in the commit?
    attributesAdded: Optional[List[ProfileAttributeMapping]] = []  # Which attributes were added ?
    attributesRemoved: Optional[List[ProfileAttributeMapping]] = []  # Which attributes were removed in the commit?
    version: str = schemas.CONTEXTS.VERSION  # What version of the system does this piece of data adhere to?
    context: str = schemas.CONTEXTS.PROFILE_COMMIT  # What is the type of the data being captured by this data type?


class RecursiveProfileCommit(NamedTuple):
    id: str  # What is the id of this piece of data? aka commitId
    createdAt: str  # When was this snapshot created?
    tenantId: str  # Which tenant does this attribute belong in?
    environmentId: str  # Which environment does this profile live in?
    profileId: str  # What profile is this commit on?
    extends: Optional[str] = None  # What is the id of the commit this commit extends?
    recursive_commits = List[ProfileCommit]
    attributesModified: Optional[List[ProfileAttributeMapping]] = []  # Which attributes were modified in the commit?
    attributesAdded: Optional[List[ProfileAttributeMapping]] = []  # Which attributes were added ?
    attributesRemoved: Optional[List[ProfileAttributeMapping]] = []  # Which attributes were removed in the commit?
    version: str = schemas.CONTEXTS.VERSION  # What version of the system does this piece of data adhere to?
    context: str = schemas.CONTEXTS.PROFILE_COMMIT  # What is the type of the data being captured by this data type?


# class ProfileCommitChain(NamedTuple):
#     """This is an in-memory data strucutre ... not found in db ... """
#     latestCommit: ProfileCommit # What is the latest commit in this commit chain?
#     additionalCommits: Optional[List[ProfileCommit]]
#     snapshot: Optional[ProfileSnapshot]



# diff on profiles is on commit chains!
#     how does the diff look like?
#     Which attributes have stayed the same?
#     Which ones have changed?
# What does the history of an attribute look lke?
#     when was it added?
#     when was it updated?
    # history(insights.liked, latestCommitId ... )

# need to be able to constuct a commit chain from a commit id!
# need to be able to freeze a commit chain into a snapshot ...


# --------------------------------------------------------------------------------

# class ProfileCommitSetAttributeContent(NamedTuple):
#     attribute: ProfileAttribute # What profile attribute are we setting?


# class ProfileCommitRemoveAttributeContent(NamedTuple):
#     profileAttributeId: str # What is the id of the profile attribute we want to remove?
#
#
# ProfileCommitContentKinds = Union[
#     ProfileCommitSetAttributeContent,
#     ProfileCommitRemoveAttributeContent
# ]


# class ProfileAttributeCommitCommand(NamedTuple):
#     """
#     Representing a commit to change an attribute in a profile.
#     # The profileId is more then a string ... its a resolvable string .. and when it gets resolved ... what should it return ...?
#     # The conceptId is more then a string ... its a resolvable string .. and when it gets resolved ... what should it return ...?
#     # The creation event tells us which "event" led to the creation of this attriubte ...
#     """
#     commitId: str # How will we reference this commit?
#     profileId: str # Who should this profile commit be applied to?
#     snapshotId: str # What snapshot of the profile id should this commit be applied to?
#     commitType: str # What kind of commit is this? How are we updaing the attribute? Are we adding a new one ... Update Attr, Remove Attr, Increment Dimensional Attribute, Decrement
#     commitContent: ProfileCommitContentKinds # What is the content of the commit? This guides commit interpretation ...
#     commited: str # When was the commit created?
#     commitor: str # Who initiated the commit? Person? Process? Skill?
#     dependsOn: List[str] # What commits does this commit depend on?
#     # summary: str # What is going on in the commit ...

# --------------------------------------------------------------------------------


# ProfileCommandKinds = Union[
#     ProfileAttributeCommitCommand,
#     Any
# ]

#
# class ProfileCommand(NamedTuple):
#     """
#     Attribute commits are not the only things that occur on profiles
#         ... they are just one type of Profile Commands
#         ... Profiles can also be cloned, reverted, merged, ...
#     """
#     commandId: str # How do we single out this command?
#     commandType: str # What type of command was initiated ..? [commit, clone, ...]
#     commandContent: ProfileCommandKinds # What is the actual content command ...?
#     initiator: str # Who initiated the command?
#     initiated: str # When was the command initiated?
#
#
# # --------------------------------------------------------------------------------


# class ProfileAttributeCommitExecutionLog(NamedTuple):
#     """
#     Representing when profile attribute commits were actually applied to profiles ...
#     """
#     profile_attribute_commit_id: str # What is the id of the commit that was applied?
#     pre_commit_profile_snapshot_id: str # What profile snapshot did we start with pre commit?
#     pre_commit_profile_attribute_content: str # What was the content of the profile attribute pre commit?
#     post_commit_profile_snapshot_id: str # What profile snapshot did we end with post commit?
#     post_commit_profile_attribute_content: str # What was the content of the profile attribute pre commit?
#     appliedOn: str # When was the commit applied?
#
#
# class ProfileCommandExecutionLog(NamedTuple):
#     """
#     Capturing chages on a profile due to commands ...
#     This can be used to revert profiles / track who did what to profiles ...
#     """
#     profile_attribute_commit_id: str # What is the id of the commit that was applied?
#     pre_commit_profile_snapshot_id: str # What profile snapshot did we start with pre commit?
#     pre_commit_profile_attribute_content: str # What was the content of the profile attribute pre commit?
#     post_commit_profile_snapshot_id: str # What profile snapshot did we end with post commit?
#     post_commit_profile_attribute_content: str # What was the content of the profile attribute pre commit?
#     appliedOn: str # When was the commit applied?
