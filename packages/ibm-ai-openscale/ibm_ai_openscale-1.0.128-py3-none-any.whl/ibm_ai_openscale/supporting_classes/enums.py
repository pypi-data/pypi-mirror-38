class MetricTypes:
    """
    Describes possible metrics types for listing deployment_metrics.

    Contains: [QUALITY_MONITORING, PERFORMANCE_MONITORING, FAIRNESS_MONITORING]
    """
    QUALITY_MONITORING = 'quality'
    PERFORMANCE_MONITORING = 'performance'
    FAIRNESS_MONITORING = 'fairness'


class Choose:
    """
    Describes possible options of choosing result from table filtering when only one result is required.

    Contains: [FIRST, LAST, RANDOM]
    """
    FIRST = 'first'
    LAST = 'last'
    RANDOM = 'random'


class ExplainabilityModelType:
    """
    For explainability, describes possible model types.

    Contains: [CLASSIFICATION, REGRESSION]
    """
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'


class ExplainabilityInputDataType:
    """
    For explainability, describes possible model input data types.

    Contains: [STRUCTURED, UNSTRUCTURED_TEXT, UNSTRUCTURED_IMAGE]
    """
    STRUCTURED = 'numeric_categorical'
    UNSTRUCTURED_IMAGE = 'image'
    UNSTRUCTURED_TEXT = 'text'


class InputDataType:
    """
    Describes possible model input data types.

    Contains: [STRUCTURED, UNSTRUCTURED_IMAGE, UNSTRUCTURED_TEXT, UNSTRUCTURED_AUDIO, UNSTRUCTURED_VIDEO]
    """
    STRUCTURED = 'structured'
    UNSTRUCTURED_IMAGE = 'unstructured_image'
    UNSTRUCTURED_TEXT = 'unstructured_text'
    UNSTRUCTURED_AUDIO = 'unstructured_audio'
    UNSTRUCTURED_VIDEO = 'unstructured_video'
