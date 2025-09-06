package com.example.evroutes.data.network

import com.example.evroutes.data.model.LoginRequest
import com.example.evroutes.data.model.LoginResponse
import com.example.evroutes.data.model.RegisterRequest
import com.example.evroutes.data.model.RegisterResponse
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.GET

interface MapApiService {
    @GET("/station/all_stations")
    suspend fun login(@Body request: LoginRequest): LoginResponse

    @POST("/auth/register")
    suspend fun register(@Body request: RegisterRequest): RegisterResponse
}