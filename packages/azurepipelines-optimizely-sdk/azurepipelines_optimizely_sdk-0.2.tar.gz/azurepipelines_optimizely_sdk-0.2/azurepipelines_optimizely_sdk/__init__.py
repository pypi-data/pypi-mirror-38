from azurepipelines_optimizely_sdk import optimizely_config_manager as ocm

class AzurePipelinesOptimizelySdk:

    def __init__(self, projectId, experimentKey):
        self.projectId = projectId
        self.experimentKey = experimentKey
        optimizelyConfigManager = ocm.OptimizelyConfigManager(projectId)
        self.optimizelyInstance = optimizelyConfigManager.getOptimizelyInstance()

    def getVariationKey(self, userId):
        variationKey = self.optimizelyInstance.activate(self.experimentKey, userId)
        return variationKey

    def trackConversionEvent(self, eventKey, userId):
        self.optimizelyInstance.track(eventKey, userId)
