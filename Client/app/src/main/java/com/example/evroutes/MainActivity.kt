package com.example.evroutes

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.evroutes.data.network.RetrofitClient
import com.example.evroutes.data.repository.AuthRepository
import com.example.evroutes.ui.auth.AuthViewModel
import com.example.evroutes.ui.auth.LoginScreen
import com.example.evroutes.ui.auth.RegisterScreen
import com.example.evroutes.ui.theme.EVRoutesTheme

// Главная активность приложения
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            EVRoutesTheme {
                EVRoutesApp()
            }
        }
    }
}

// Настройка навигации приложения
@Composable
fun EVRoutesApp() {
    val navController = rememberNavController()
    val authRepository = AuthRepository(RetrofitClient.authApiService)
    val authViewModel = AuthViewModel(authRepository)

    NavHost(navController = navController, startDestination = "login") {
        composable("login") {
            LoginScreen(viewModel = authViewModel, navController = navController)
        }
        composable("register") {
            RegisterScreen(viewModel = authViewModel, navController = navController)
        }
    }
}