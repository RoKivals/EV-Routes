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

private fun buildRoute(startPoint, endPoint, consumption: Float, initialBattery: Float, minBatteryPercent: Float) {
    // Параметры запроса
    val request = RouteRequest(
        start = Coordinates(startPoint.latitude, startPoint.longitude),
        end = Coordinates(endPoint.latitude, endPoint.longitude),
        initial_battery = initialBattery,
        min_battery_percent = minBatteryPercent,
        consumption_per_km = consumption,
        charging_stations = getPredefinedChargingStations() // Предопределенные станции
    )
    
    _uiState.value = _uiState.value.copy(isLoading = true)
    
    routeService.calculateRoute(request).enqueue(object : Callback<RouteResponse> {
        override fun onResponse(call: Call<RouteResponse>, response: Response<RouteResponse>) {
            if (response.isSuccessful && response.body()?.success == true) {
                val routeResponse = response.body()!!
                
                // Обновляем UI
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = null,
                    routeInfo = "Расстояние: ${routeResponse.total_distance} км, " +
                              "Финальный заряд: ${routeResponse.final_battery}%"
                )
                
                // Отображаем маршрут на карте
                displayOptimizedRoute(routeResponse)
                
                // Рассчитываем расход энергии
                calculateEnergyConsumption(routeResponse.total_distance, consumption)
            } else {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = "Ошибка сервера: ${response.errorBody()?.string()}"
                )
            }
        }
        
        override fun onFailure(call: Call<RouteResponse>, t: Throwable) {
            _uiState.value = _uiState.value.copy(
                isLoading = false,
                error = "Ошибка сети: ${t.message}"
            )
        }
    })
}

private fun displayOptimizedRoute(routeResponse: RouteResponse) {
    mapView?.map?.let { map ->
        map.mapObjects.clear()
        val mapObjectCollection = map.mapObjects.addCollection()
        
        // Рисуем маршрут
        val points = routeResponse.path_coordinates.map { Point(it.lat, it.lon) }
        mapObjectCollection.addPolyline(points).apply {
            setStrokeColor(0xFF0066FF.toInt())
            setStrokeWidth(5.0f)
        }
        
        // Добавляем маркеры
        points.forEachIndexed { index, point ->
            mapObjectCollection.addPlacemark().apply {
                geometry = point
                when {
                    index == 0 -> setIcon(ImageProvider.fromBitmap(createCircleBitmap(Color.GREEN, 40)))
                    index == points.size - 1 -> setIcon(ImageProvider.fromBitmap(createCircleBitmap(Color.RED, 40)))
                    routeResponse.charging_stations.any { it.id == index } -> 
                        setIcon(ImageProvider.fromBitmap(createChargingStationBitmap(Color.BLUE, 35)))
                    else -> setIcon(ImageProvider.fromBitmap(createCircleBitmap(Color.YELLOW, 30)))
                }
            }
        }
        
        // Центрируем камеру
        val boundingBox = BoundingBox.builder()
            .include(points)
            .build()
        map.move(CameraPosition(boundingBox), Animation(Animation.Type.SMOOTH, 1f))
    }
}

// Интерфейс для API
interface RouteService {
    @POST("calculate_route")
    fun calculateRoute(@Body request: RouteRequest): Call<RouteResponse>
}

// Модели данных
data class RouteRequest(
    val start: Coordinates,
    val end: Coordinates,
    val initial_battery: Float,
    val min_battery_percent: Float,
    val consumption_per_km: Float,
    val charging_stations: List<ChargingStation>
)

data class RouteResponse(
    val success: Boolean,
    val total_distance: Float,
    val path_coordinates: List<Coordinates>,
    val charging_stations: List<ChargingStation>,
    val final_battery: Float
)

data class Coordinates(val lat: Double, val lon: Double)

data class ChargingStation(
    val id: Int,
    val lat: Double,
    val lon: Double,
    val name: String
)

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