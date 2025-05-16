package com.example.evroutes.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.evroutes.data.repository.AuthRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

// ViewModel для управления состоянием UI авторизации
class AuthViewModel(private val repository: AuthRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(AuthUiState())
    val uiState: StateFlow<AuthUiState> = _uiState.asStateFlow()

    fun login(email: String, password: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            val result = repository.login(email, password)
            _uiState.value = when {
                result.isSuccess -> _uiState.value.copy(isLoading = false, token = result.getOrNull(), error = null)
                else -> _uiState.value.copy(isLoading = false, error = result.exceptionOrNull()?.message ?: "Ошибка входа")
            }
        }
    }

    fun register(email: String, password: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            val result = repository.register(email, password)
            _uiState.value = when {
                result.isSuccess -> _uiState.value.copy(isLoading = false, token = null, error = null, isRegistered = true)
                else -> _uiState.value.copy(isLoading = false, error = result.exceptionOrNull()?.message ?: "Ошибка регистрации")
            }
        }
    }

    fun resetState() {
        _uiState.value = AuthUiState()
    }
}

// Модель состояния UI
data class AuthUiState(
    val isLoading: Boolean = false,
    val token: String? = null,
    val error: String? = null,
    val isRegistered: Boolean = false
)