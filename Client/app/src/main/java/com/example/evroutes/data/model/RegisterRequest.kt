package com.example.evroutes.data.model

data class RegisterRequest(
    val email: String,
    val password: String,
    val role: String = "user"
)
