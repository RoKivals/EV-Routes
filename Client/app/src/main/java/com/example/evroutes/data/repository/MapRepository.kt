package com.example.evroutes.data.repository

import com.example.evroutes.data.network.MapApiService
import com.yandex.mapkit.RequestPoint
import com.yandex.mapkit.RequestPointType
import com.yandex.mapkit.directions.DirectionsFactory
import com.yandex.mapkit.directions.driving.DrivingOptions
import com.yandex.mapkit.directions.driving.DrivingRoute
import com.yandex.mapkit.directions.driving.DrivingRouter
import com.yandex.mapkit.directions.driving.DrivingRouterType
import com.yandex.mapkit.directions.driving.DrivingSession
import com.yandex.mapkit.directions.driving.VehicleOptions
import com.yandex.mapkit.directions.driving.VehicleType
import com.yandex.mapkit.geometry.Point

class MapRepository(private val apiService: MapApiService) {
    private val drivingRouter: DrivingRouter =
        DirectionsFactory.getInstance().createDrivingRouter(DrivingRouterType.ONLINE)

    fun findRoute(
        from: Point,
        to: Point,
        onSuccess: (DrivingSession.DrivingRouteListener) -> Unit,
        onError: (Exception) -> Unit
    ) {
        try {
            val requestPoints = listOf(
                RequestPoint(from, RequestPointType.WAYPOINT, null, null, null),
                RequestPoint(to, RequestPointType.WAYPOINT, null, null, null)
            )

            val drivingOptions = DrivingOptions().apply {
                routesCount = 1
            }

            val vehicleOptions = VehicleOptions().setVehicleType(VehicleType.DEFAULT)

            val routeListener = object : DrivingSession.DrivingRouteListener {
                override fun onDrivingRoutes(routes: MutableList<DrivingRoute>) {
                    if (routes.isNotEmpty()) {
                        onSuccess(this)
                    } else {
                        onError(Exception("Маршрут не найден"))
                    }
                }

                override fun onDrivingRoutesError(error: com.yandex.runtime.Error) {
                    onError(Exception("Ошибка построения маршрута: ${error.toString()}"))
                }
            }

            drivingRouter.requestRoutes(requestPoints, drivingOptions, vehicleOptions, routeListener)

        } catch (e: Exception) {
            onError(e)
        }
    }

    suspend fun getCurrentLocation(): Result<Point> {
        return try {
            val currentLocation = Point(55.751574, 37.573856)
            Result.success(currentLocation)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

}