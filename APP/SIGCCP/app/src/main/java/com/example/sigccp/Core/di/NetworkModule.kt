package com.example.sigccp.Core.di
//APP/SIGCCP/app/src/main/java/com/example/sigccp/Core/di/NetworkModule.kt
import com.example.sigccp.activity.pedido.Data.Network.ApiServicePedido
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton


@Module
@InstallIn(SingletonComponent::class)
class NetworkModule {

    //inyectamos retrofit
    @Singleton
    @Provides
    fun provideApiService(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://35.238.195.112:3000/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    //Inyectamos las interface de los endpoints
    @Singleton
    @Provides
    fun provideApiServicePedido(retrofit: Retrofit): ApiServicePedido {
        return retrofit.create(ApiServicePedido::class.java)
    }

/*
    @Singleton
    @Provides
    fun provideApiServiceProducto(retrofit: Retrofit): ApiServiceProducto {
        return retrofit.create(ApiServiceProducto::class.java)
    }

    @Singleton
    @Provides
    fun provideApiServiceCliente(retrofit: Retrofit): ApiServiceCliente {
        return retrofit.create(ApiServiceCliente::class.java)
    }
*/
}