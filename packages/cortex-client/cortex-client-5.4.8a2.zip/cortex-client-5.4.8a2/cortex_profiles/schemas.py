from typing import NamedTuple


class _CONTEXTS(NamedTuple):
    VERSION :str = "0.0.1"
    SESSION :str = "cortex/session"
    INSIGHT :str = "cortex/insight"
    INSIGHT_CONCEPT_TAG :str = "cortex/insight-concept-tag"
    INSIGHT_TAG_RELATIONSHIP :str = "cortex/insight-concept-relationship"
    INSIGHT_TAG_RELATED_TO_RELATIONSHIP : str = "cortex/insight-relatedTo-concept"
    INSIGHT_INTERACTION : str = "cortex/insight-interaction"
    PROFILE_SNAPSHOT: str = "cortex/profile-snapshot"
    PROFILE: str = "cortex/profile"
    PROFILE_COMMIT : str = "cortex/profile-commit"

    DECLARED_PROFILE_ATTRIBUTE: str = "cortex/profile-attributes/declared"
    OBSERVED_PROFILE_ATTRIBUTE: str = "cortex/profile-attributes/observed"
    INFERRED_PROFILE_ATTRIBUTE: str = "cortex/profile-attributes/inferred"

    END_USER_PROFILE: str = "cortex/end_user_profile"

    RELATIONSHIP_PROFILE_ATTRIBUTE_VALUE: str = "cortex/profile-attribute-value/relationship"
    OBJECT_PROFILE_ATTRIBUTE_VALUE: str = "cortex/profile-attribute-value/object"
    NUMERICAL_PROFILE_ATTRIBUTE_VALUE : str = "cortex/profile-attribute-values/numerical"
    PERCENTILE_PROFILE_ATTRIBUTE_VALUE: str = "cortex/profile-attribute-value/percentile"
    AVERAGE_PROFILE_ATTRIBUTE_VALUE: str = "cortex/profile-attribute-value/average"
    TOTAL_PROFILE_ATTRIBUTE_VALUE: str = "cortex/profile-attribute-value/total"
    COUNTER_PROFILE_ATTRIBUTE_VALUE: str = "cortex/profile-attribute-value/counter"
    CLASSIFICATION_PROFILE_ATTRIBUTE_VALUE: str = "cortex/profile-attribute-value/classification"
    DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE : str = "cortex/profile-attribute-value/dimensional"
    # ??? DECLARED_PROFILE_ATTRIBUTE_VALUE: str = "cortex/declared-profile-attribute-value"  # Declared Strings vs Declared Counters ...

    DAY:str="cortex/time/day"


CONTEXTS = _CONTEXTS()


# ===========


class _INTERACTIONS(NamedTuple):
    CONTEXT:str= CONTEXTS.INSIGHT_INTERACTION
    PRESENTED:str="presented"
    VIEWED:str="viewed"
    IGNORED:str="ignored"
    STARTED_INTERACTION:str="startedInteractionISOUTC"
    STOPPED_INTERACTION:str="stoppedInteractionISOUTC"


INTERACTIONS = _INTERACTIONS()

# ===========


class _INSIGHT_COLS(NamedTuple):
    CONTEXT:str="context"
    ID:str="id"
    APPID:str="appId"
    TAGS:str="tags"
    INSIGHTTYPE:str="insightType"
    PROFILEID:str="profileId"
    DATEGENERATEDUTCISO:str="dateGeneratedUTCISO"


# TODO - Ensure this is insync with the sessions model
class _SESSIONS_COLS(NamedTuple):
    CONTEXT:str="context"
    ID:str="id"
    ISOUTCENDTIME:str="isoUTCStartTime"
    ISOUTCSTARTTIME:str= "isoUTCEndTime"
    PROFILEID:str="profileId"
    APPID:str="appId"
    DURATIONINSECONDS:str="durationInSeconds"


class _INTERACTIONS_COLS(NamedTuple):
    CONTEXT:str="context"
    ID:str="id"
    INTERACTIONTYPE:str="interactionType"
    INSIGHTID:str="insightId"
    PROFILEID:str="profileId"
    SESSIONID:str="sessionId"
    INTERACTIONDATEISOUTC:str="interactionDateISOUTC"
    PROPERTIES:str="properties"
    CUSTOM:str="custom"


class _COUNT_OF_INTERACTIONS_COL(NamedTuple):
    PROFILEID:str="profileId"
    INSIGHTTYPE:str="insightType"
    INTERACTIONTYPE:str="interactionType"
    TOTAL:str="total"


class _COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL(NamedTuple):
    PROFILEID:str="profileId"
    INSIGHTTYPE:str="insightType"
    INTERACTIONTYPE:str="interactionType"
    TAGGEDCONCEPTTYPE:str="taggedConceptType"
    TAGGEDCONCEPTRELATIONSHIP:str="taggedConceptRelationship"
    TAGGEDCONCEPTID:str="taggedConceptId"
    TAGGEDCONCEPTTITLE:str="taggedConceptTitle"
    TAGGEDON:str="taggedOn"
    TOTAL:str="total"


class _TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL(NamedTuple):
    PROFILEID: str = "profileId"
    INSIGHTTYPE: str = "insightType"
    INTERACTIONTYPE: str = "interactionType"
    TAGGEDCONCEPTTYPE: str = "taggedConceptType"
    TAGGEDCONCEPTRELATIONSHIP: str = "taggedConceptRelationship"
    TAGGEDCONCEPTID: str = "taggedConceptId"
    TAGGEDCONCEPTTITLE: str = "taggedConceptTitle"
    TAGGEDON: str = "taggedOn"
    ISOUTCSTARTTIME: str =  INTERACTIONS.STARTED_INTERACTION
    ISOUTCENDTIME: str = INTERACTIONS.STOPPED_INTERACTION
    TOTAL: str = "duration_in_seconds"


# ===========


INSIGHT_COLS = _INSIGHT_COLS()
SESSIONS_COLS = _SESSIONS_COLS()
INTERACTIONS_COLS = _INTERACTIONS_COLS()
COUNT_OF_INTERACTIONS_COL = _COUNT_OF_INTERACTIONS_COL()
COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL = _COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL()
TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL = _TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL()


# ===========

class _INSIGHT_ACTIVITY_COLS(NamedTuple):
    ACTIVITY_TIME:str="isoUTCActivityTime"
    APPID:str=SESSIONS_COLS.APPID
    PROFILEID:str=SESSIONS_COLS.PROFILEID
    ISOUTCSTARTTIME:str=SESSIONS_COLS.ISOUTCSTARTTIME
    ISOUTCENDTIME: str = SESSIONS_COLS.ISOUTCENDTIME

class _LOGIN_COUNTS_COL(NamedTuple):
    CONTEXT:str="context"
    ID:str="id"
    APPID:str="appId"
    PROFILEID:str="profileId"
    TOTAL:str="total_logins"


class _LOGIN_DURATIONS_COL(NamedTuple):
    CONTEXT:str="context"
    ID:str="id"
    APPID:str="appId"
    PROFILEID:str="profileId"
    DURATION:str=SESSIONS_COLS.DURATIONINSECONDS


class _DAILY_LOGIN_COUNTS_COL(NamedTuple):
    CONTEXT:str="context"
    ID:str="id"
    APPID:str="appId"
    PROFILEID:str="profileId"
    TOTAL:str="total_logins"
    DAY:str="day"


class _DAILY_LOGIN_DURATIONS_COL(NamedTuple):
    CONTEXT:str="context"
    ID:str="id"
    APPID:str="appId"
    PROFILEID:str="profileId"
    DURATION:str=SESSIONS_COLS.DURATIONINSECONDS
    DAY: str = "day"


# ===========

INSIGHT_ACTIVITY_COLS = _INSIGHT_ACTIVITY_COLS()
LOGIN_COUNTS_COL = _LOGIN_COUNTS_COL()
LOGIN_DURATIONS_COL = _LOGIN_DURATIONS_COL()
DAILY_LOGIN_COUNTS_COL = _DAILY_LOGIN_COUNTS_COL()
DAILY_LOGIN_DURATIONS_COL = _DAILY_LOGIN_DURATIONS_COL()


# ===========


INSIGHTS_PRESENTED_PER_INSIGHTT_TYPE = "insights.presented.perInsightType.total"
INSIGHTS_VIEWED_PER_INSIGHTT_TYPE = "insights.viewed.perInsightType.total"
INSIGHTS_IGNORED_PER_INSIGHTT_TYPE = "insights.ignored.perInsightType.total"

INSIGHTS_PRESENTED_RECENTLY_PER_INSIGHTT_TYPE = "insights.recentlyPresented.perInsightType.total"
INSIGHTS_VIEWED_RECENTLY_PER_INSIGHTT_TYPE = "insights.recentlyViewed.perInsightType.total"
INSIGHTS_IGNORED_RECENTLY_PER_INSIGHTT_TYPE = "insights.recentlyIgnored.perInsightType.total"


#  =========


INSIGHTS_PRESENTED_RELATED_TO_COMPANIES = "insights.presented.relatedToCompanies.total"
INSIGHTS_PRESENTED_RELATED_TO_SECTORS = "insights.presented.relatedToSectors.total"
INSIGHTS_PRESENTED_RELATED_TO_MARKET_INDICES = "insights.presented.relatedToMarketIndices.total"
INSIGHTS_PRESENTED_RELATED_TO_COUNTRIES = "insights.presented.relatedToCountriesOfExchanges.total"

INSIGHTS_PRESENTED_RECENTLY_RELATED_TO_COMPANIES = "insights.recentlyPresented.relatedToCompanies.total"
INSIGHTS_PRESENTED_RECENTLY_RELATED_TO_SECTORS = "insights.recentlyPresented.relatedToSectors.total"
INSIGHTS_PRESENTED_RECENTLY_RELATED_TO_MARKET_INDICES = "insights.recentlyPresented.relatedToMarketIndices.total"
INSIGHTS_PRESENTED_RECENTLY_RELATED_TO_COUNTRIES = "insights.recentlyPresented.relatedToCountriesOfExchanges.total"

#  =========


INSIGHTS_VIEWED_RELATED_TO_COMPANIES = "insights.viewed.relatedToCompanies.total"
INSIGHTS_VIEWED_RELATED_TO_SECTORS = "insights.viewed.relatedToSectors.total"
INSIGHTS_VIEWED_RELATED_TO_MARKET_INDICES = "insights.viewed.relatedToMarketIndices.total"
INSIGHTS_VIEWED_RELATED_TO_COUNTRIES = "insights.viewed.relatedToCountriesOfExchanges.total"

INSIGHTS_VIEWED_RECENTLY_RELATED_TO_COMPANIES = "insights.recentlyViewed.relatedToCompanies.total"
INSIGHTS_VIEWED_RECENTLY_RELATED_TO_SECTORS = "insights.recentlyViewed.relatedToSectors.total"
INSIGHTS_VIEWED_RECENTLY_RELATED_TO_MARKET_INDICES = "insights.recentlyViewed.relatedToMarketIndices.total"
INSIGHTS_VIEWED_RECENTLY_RELATED_TO_COUNTRIES = "insights.recentlyViewed.relatedToCountriesOfExchanges.total"


#  =========


INSIGHTS_IGNORED_RELATED_TO_COMPANIES = "insights.ignored.relatedToCompanies.total"
INSIGHTS_IGNORED_RELATED_TO_SECTORS = "insights.ignored.relatedToSectors.total"
INSIGHTS_IGNORED_RELATED_TO_MARKET_INDICES = "insights.ignored.relatedToMarketIndices.total"
INSIGHTS_IGNORED_RELATED_TO_COUNTRIES = "insights.ignored.relatedToCountriesOfExchanges.total"

INSIGHTS_IGNORED_RECENTLY_RELATED_TO_COMPANIES = "insights.recentlyIgnored.relatedToCompanies.total"
INSIGHTS_IGNORED_RECENTLY_RELATED_TO_SECTORS = "insights.recentlyIgnored.relatedToSectors.total"
INSIGHTS_IGNORED_RECENTLY_RELATED_TO_MARKET_INDICES = "insights.recentlyIgnored.relatedToMarketIndices.total"
INSIGHTS_IGNORED_RECENTLY_RELATED_TO_COUNTRIES = "insights.recentlyIgnored.relatedToCountriesOfExchanges.total"


#  =========


TIME_SPENT_ON_INSIGHTS_RELATED_TO_COMPANIES = "insights.duration.relatedToCompanies.total"
TIME_SPENT_ON_INSIGHTS_RELATED_TO_SECTORS = "insights.duration.relatedToSectors.total"
TIME_SPENT_ON_INSIGHTS_RELATED_TO_MARKET_INDICES = "insights.duration.relatedToMarketIndices.total"
TIME_SPENT_ON_INSIGHTS_RELATED_TO_COUNTRIES = "insights.duration.relatedToCountriesOfExchanges.total"


#  =========


LOGINS_DURATION_TOTAL = "logins.duration.appSpecific.total"
LOGINS_RECENT_DURATION_TOTAL = "logins.recentDuration.appSpecific.total"

LOGINS_DAILY_DURATION_TOTAL = "logins.dailyDuration.appSpecific.total"
LOGINS_RECENT_DAILY_DURATION_TOTAL = "logins.recentDailyDuration.appSpecific.total"

LOGINS_DAILY_DURATION_AVERAGE = "logins.dailyDuration.appSpecific.average"
LOGINS_RECENT_DAILY_DURATION_AVERAGE = "logins.recentDailyDuration.appSpecific.average"

LOGINS_TOTAL = "logins.instances.appSpecific.total"
LOGINS_RECENT_TOTAL = "logins.recentInstances.appSpecific.total"

LOGINS_DAILY_TOTALS = "logins.dailyInstances.appSpecific.total"
LOGINS_RECENT_DAILY_TOTALS = "logins.recentDailyInstances.appSpecific.total"

LOGINS_DAILY_AVERAGE = "logins.dailyInstances.appSpecific.average"
LOGINS_RECENT_DAILY_AVERAGE = "logins.recentDailyInstances.appSpecific.average"

# ==========

# TODO - [ ] Attribute to derive ... time spent on all insights ...
