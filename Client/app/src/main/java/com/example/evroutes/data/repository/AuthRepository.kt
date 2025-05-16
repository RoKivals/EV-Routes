package com.example.evroutes.data.repository

import com.example.evroutes.data.model.LoginRequest
import com.example.evroutes.data.model.RegisterRequest
import com.example.evroutes.data.network.AuthApiService

class AuthRepository(private val apiService: AuthApiService) {
    suspend fun login(email: String, password: String): Result<String> {
        return try {
            val response = apiService.login(LoginRequest(email, password))
            Result.success(response.access_token)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun register(email: String, password: String): Result<String> {
        return try {
            val response = apiService.register(RegisterRequest(email, password))
            Result.success(response.status)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}