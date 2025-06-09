package com.example.evroutes.ui.map

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.evroutes.data.repository.MapRepository
import com.yandex.mapkit.geometry.Point
import com.yandex.mapkit.map.CameraPosition
import com.yandex.mapkit.mapview.MapView
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

import com.yandex.mapkit.directions.DirectionsFactory
import com.yandex.mapkit.directions.driving.DrivingOptions
import com.yandex.mapkit.directions.driving.DrivingRoute
import com.yandex.mapkit.directions.driving.DrivingRouter
import com.yandex.mapkit.directions.driving.DrivingSession
import com.yandex.mapkit.directions.driving.VehicleOptions
import com.yandex.mapkit.RequestPoint
import com.yandex.mapkit.RequestPointType
import com.yandex.mapkit.directions.driving.DrivingRouterType
import com.yandex.runtime.image.ImageProvider
import android.graphics.Color

import android.graphics.*

data class MapUiState(
    val isLoading: Boolean = false,
    val error: String? = null,
    val cameraPosition: CameraPosition = CameraPosition(
        Point(55.751574, 37.573856), // Москва по умолчанию
        11.0f, 0.0f, 0.0f
    ),
    val chargingStations: List<Point> = emptyList(),
    val selectedStation: Point? = null,
    val userLocation: Point? = null
)

class MapViewModel(
    private val mapRepository: MapRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(MapUiState())
    val uiState: StateFlow<MapUiState> = _uiState.asStateFlow()

    private var mapView: MapView? = null

    fun setMapView(mapView: MapView) {
        this.mapView = mapView
        // loadChargingStations()
    }

    fun moveToUserLocation() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)

            try {
                // Здесь будет логика получения текущей локации пользователя
                // Для примера используем координаты Москвы
                val userLocation = Point(55.751574, 37.573856)

                _uiState.value = _uiState.value.copy(
                    userLocation = userLocation,
                    cameraPosition = CameraPosition(userLocation, 15.0f, 0.0f, 0.0f),
                    isLoading = false
                )

                // Перемещение камеры к позиции пользователя
                mapView?.map?.move(
                    CameraPosition(userLocation, 15.0f, 0.0f, 0.0f)
                )

            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    error = "Не удалось определить местоположение: ${e.message}",
                    isLoading = false
                )
            }
        }
    }

    fun buildRouteWithParams(startPoint: String, endPoint: String, consumption: Float) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)

            try {
                buildMoscowToSpbRoute(consumption)
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    error = "Ошибка построения маршрута: ${e.message}",
                    isLoading = false
                )
            }
        }
    }

    private fun buildMoscowToSpbRoute(consumption: Float) {
        val drivingRouter: DrivingRouter = DirectionsFactory.getInstance().createDrivingRouter(
            DrivingRouterType.ONLINE)

        // Определяем точки маршрута
        val requestPoints = listOf(
            RequestPoint(
                Point(55.751574, 37.573856), // Москва (стартовая точка)
                RequestPointType.WAYPOINT,
                null, null, null
            ),
            RequestPoint(
                Point(57.03216, 34.98807), // Первая промежуточная точка
                RequestPointType.WAYPOINT,
                null, null, null
            ),
            RequestPoint(
                Point(58.75839, 31.50041), // Вторая промежуточная точка
                RequestPointType.WAYPOINT,
                null, null, null
            ),
            RequestPoint(
                Point(59.93428, 30.33514), // Санкт-Петербург (конечная точка)
                RequestPointType.WAYPOINT,
                null, null, null
            )
        )

        // Настройки для маршрута
        val drivingOptions = DrivingOptions().apply {
            // Можно настроить опции маршрутизации
            routesCount = 1 // Строим только один маршрут
        }

        // Настройки транспортного средства (для электромобиля)
        val vehicleOptions = VehicleOptions().apply {
            // Здесь можно указать параметры электромобиля
            // vehicleType = VehicleType.ELECTRIC (если доступно)
        }

        // Строим маршрут
        val drivingSession = drivingRouter.requestRoutes(
            requestPoints,
            drivingOptions,
            vehicleOptions,
            object : DrivingSession.DrivingRouteListener {
                override fun onDrivingRoutes(routes: MutableList<DrivingRoute>) {
                    // Успешно построен маршрут
                    if (routes.isNotEmpty()) {
                        val route = routes[0]

                        // Обновляем состояние UI
                        _uiState.value = _uiState.value.copy(
                            isLoading = false,
                            error = null
                        )

                        // Добавляем маршрут на карту
                        addRouteToMap(route)

                        // Вычисляем расход энергии для маршрута
                        calculateEnergyConsumption(route, consumption)

                    } else {
                        _uiState.value = _uiState.value.copy(
                            error = "Не удалось построить маршрут",
                            isLoading = false
                        )
                    }
                }

                override fun onDrivingRoutesError(error: com.yandex.runtime.Error) {
                    _uiState.value = _uiState.value.copy(
                        error = "Ошибка построения маршрута: ${error.toString()}",
                        isLoading = false
                    )
                }
            }
        )
    }

    private fun addRouteToMap(route: DrivingRoute) {
        mapView?.map?.let { map ->
            map.mapObjects.clear()

            val mapObjectCollection = map.mapObjects.addCollection()

            mapObjectCollection.addPolyline(route.geometry).apply {
                setStrokeColor(0xFF0066FF.toInt()) // или Color.BLUE
                setStrokeWidth(5.0f)
            }

            val points = listOf(
                Point(55.751574, 37.573856), // Москва
                Point(57.03216, 34.98807),   // Промежуточная 1
                Point(58.75839, 31.50041),   // Промежуточная 2
                Point(59.93428, 30.33514)    // СПб
            )

            points.forEachIndexed { index, point ->
                mapObjectCollection.addPlacemark().apply {
                    geometry = point
                    when (index) {
                        0 -> {
                            // Стартовая точка - зеленый круг
                            setIcon(ImageProvider.fromBitmap(createCircleBitmap(Color.GREEN, 40)))
                        }
                        points.size - 1 -> {
                            // Конечная точка - красный круг
                            setIcon(ImageProvider.fromBitmap(createCircleBitmap(Color.RED, 40)))
                        }
                        else -> {
                            // Промежуточные точки - желтый круг
                            setIcon(ImageProvider.fromBitmap(createCircleBitmap(Color.YELLOW, 35)))
                        }
                    }
                }
            }

            // Центрируем камеру
            val centerPoint = Point(57.5, 34.0)
            val cameraPosition = CameraPosition(centerPoint, 6.0f, 0.0f, 0.0f)
            map.move(cameraPosition)
        }
    }

    // Вспомогательная функция для создания цветного круга
    private fun createCircleBitmap(color: Int, size: Int): Bitmap {
        val bitmap = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bitmap)
        val paint = Paint().apply {
            this.color = color
            isAntiAlias = true
            style = Paint.Style.FILL
        }

        // Рисуем круг с белой обводкой
        val radius = size / 2f
        val center = radius

        // Белая обводка
        paint.color = Color.WHITE
        canvas.drawCircle(center, center, radius, paint)

        // Цветной круг внутри
        paint.color = color
        canvas.drawCircle(center, center, radius - 4, paint)

        return bitmap
    }

    private fun calculateEnergyConsumption(route: DrivingRoute, consumptionPer100km: Float) {
        // Получаем общее расстояние маршрута в метрах
        val totalDistanceMeters = route.metadata.weight.distance.value
        val totalDistanceKm = totalDistanceMeters / 1000.0

        // Вычисляем общий расход энергии
        val totalConsumption = (totalDistanceKm * consumptionPer100km / 100.0).toFloat()

        // Здесь можно обновить UI состояние с информацией о маршруте
        // Например, добавить в MapUiState поля для отображения информации о маршруте

        // Логируем для отладки
        println("Общее расстояние: ${String.format("%.1f", totalDistanceKm)} км")
        println("Расход энергии: ${String.format("%.1f", totalConsumption)} кВт⋅ч")
        println("Время в пути: ${route.metadata.weight.time.text}")
    }

    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }
}