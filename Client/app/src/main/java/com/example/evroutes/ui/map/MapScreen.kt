package com.example.evroutes.ui.map

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.navigation.NavController
import com.yandex.mapkit.geometry.Point
import com.yandex.mapkit.map.CameraPosition
import com.yandex.mapkit.mapview.MapView

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MapScreen(
    navController: NavController,
    viewModel: MapViewModel // Создадим позже
) {
    var mapView by remember { mutableStateOf<MapView?>(null) }
    var showRouteDialog by remember { mutableStateOf(false) }

    val uiState by viewModel.uiState.collectAsState()

    Box(modifier = Modifier.fillMaxSize()) {
        // Карта занимает весь экран
        YandexMapView(
            modifier = Modifier.fillMaxSize(),
            onMapReady = { map ->
                mapView = map
                viewModel.setMapView(map)
            },
            cameraPosition = uiState.cameraPosition
        )

        // Кнопки управления снизу
        Card(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .padding(16.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                // Кнопка "Моя локация"
                FloatingActionButton(
                    onClick = { viewModel.moveToUserLocation() },
                    containerColor = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(56.dp)
                ) {
                    Icon(
                        Icons.Default.LocationOn,
                        contentDescription = "Моя локация",
                        tint = Color.White
                    )
                }

                // Кнопка "Найти маршрут"
                Button(
                    onClick = { showRouteDialog = true },
                    modifier = Modifier
                        .weight(1f)
                        .padding(start = 16.dp),
                    enabled = !uiState.isLoading
                ) {
                    Text("Построить маршрут")
                }
            }
        }

        // Индикатор загрузки
        if (uiState.isLoading) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Card(
                    elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
                ) {
                    Column(
                        modifier = Modifier.padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        CircularProgressIndicator()
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Поиск маршрута...")
                    }
                }
            }
        }

        // Отображение ошибок
        uiState.error?.let { error ->
            LaunchedEffect(error) {
                // Показать Snackbar с ошибкой
            }
        }

        if (showRouteDialog) {
            RouteDialog(
                onDismiss = { showRouteDialog = false },
                onBuildRoute = { startPoint, endPoint, consumption ->
                    showRouteDialog = false
                    val consumptionFloat = consumption.toFloatOrNull() ?: 20.0f
                    viewModel.buildRouteWithParams(startPoint, endPoint, consumptionFloat)
                },
                currentLocation = uiState.userLocation
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RouteDialog(
    onDismiss: () -> Unit,
    onBuildRoute: (String, String, String) -> Unit,
    currentLocation: Point?
) {
    var startPoint by remember { mutableStateOf("") }
    var endPoint by remember { mutableStateOf("") }
    var consumption by remember { mutableStateOf("") }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(
            dismissOnBackPress = true,
            dismissOnClickOutside = true
        )
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
        ) {
            Column(
                modifier = Modifier.padding(24.dp)
            ) {
                // Заголовок с кнопкой закрытия
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Построение маршрута",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold
                    )

                    IconButton(
                        onClick = onDismiss
                    ) {
                        Icon(
                            Icons.Default.Close,
                            contentDescription = "Закрыть"
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Поле исходной точки
                OutlinedTextField(
                    value = startPoint,
                    onValueChange = { startPoint = it },
                    label = { Text("Исходная точка") },
                    placeholder = { Text("Введите адрес или координаты") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )

                Spacer(modifier = Modifier.height(12.dp))

                // Поле конечной точки
                OutlinedTextField(
                    value = endPoint,
                    onValueChange = { endPoint = it },
                    label = { Text("Конечная точка") },
                    placeholder = { Text("Введите адрес или координаты") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )

                Spacer(modifier = Modifier.height(12.dp))

                // Поле расхода автомобиля
                OutlinedTextField(
                    value = consumption,
                    onValueChange = {
                        // Позволяем вводить только цифры и точку
                        if (it.isEmpty() || it.matches(Regex("^\\d*\\.?\\d*$"))) {
                            consumption = it
                        }
                    },
                    label = { Text("Средний расход") },
                    placeholder = { Text("кВт⋅ч/100км") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                    supportingText = { Text("Расход электроэнергии в кВт⋅ч на 100 км") }
                )

                Spacer(modifier = Modifier.height(24.dp))

                // Кнопки
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    OutlinedButton(
                        onClick = onDismiss,
                        modifier = Modifier.weight(1f)
                    ) {
                        Text("Отмена")
                    }

                    Button(
                        onClick = {
                            if (startPoint.isNotBlank() && endPoint.isNotBlank() && consumption.isNotBlank()) {
                                onBuildRoute(startPoint, endPoint, consumption)
                            }
                        },
                        modifier = Modifier.weight(1f),
                        enabled = startPoint.isNotBlank() && endPoint.isNotBlank() && consumption.isNotBlank()
                    ) {
                        Text("Построить")
                    }
                }
            }
        }
    }
}