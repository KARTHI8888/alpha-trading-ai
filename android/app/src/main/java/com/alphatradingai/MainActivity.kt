package com.alphatradingai

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Rect
import android.net.Uri
import android.os.Bundle
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.util.Base64
import android.webkit.JavascriptInterface
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.view.PixelCopy
import java.io.ByteArrayOutputStream

class MainActivity : Activity() {

    private lateinit var webView: WebView
    private var filePathCallback: ValueCallback<Array<Uri>>? = null

    companion object {
        private const val FILE_CHOOSER_REQUEST = 1001
    }

    private fun deliverBitmap(bitmap: Bitmap) {
        val output = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 85, output)
        bitmap.recycle()

        val encoded = Base64.encodeToString(
            output.toByteArray(),
            Base64.NO_WRAP
        )

        webView.evaluateJavascript(
            "window.onNativeChartCaptured && window.onNativeChartCaptured('$encoded')",
            null
        )
    }

    private fun captureFallback() {
        val bitmap = Bitmap.createBitmap(
            webView.width,
            webView.height,
            Bitmap.Config.ARGB_8888
        )
        webView.draw(Canvas(bitmap))
        deliverBitmap(bitmap)
    }

    inner class ChartBridge {
        @JavascriptInterface
        fun captureChart() {
            runOnUiThread {
                if (!::webView.isInitialized ||
                    webView.width <= 0 || webView.height <= 0
                ) return@runOnUiThread

                if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
                    captureFallback()
                    return@runOnUiThread
                }

                val bitmap = Bitmap.createBitmap(
                    webView.width,
                    webView.height,
                    Bitmap.Config.ARGB_8888
                )

                val location = IntArray(2)
                webView.getLocationInWindow(location)

                val rect = Rect(
                    location[0],
                    location[1],
                    location[0] + webView.width,
                    location[1] + webView.height
                )

                PixelCopy.request(
                    window,
                    rect,
                    bitmap,
                    { result ->
                        if (result == PixelCopy.SUCCESS) {
                            deliverBitmap(bitmap)
                        } else {
                            bitmap.recycle()
                            captureFallback()
                        }
                    },
                    Handler(Looper.getMainLooper())
                )
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            loadWithOverviewMode = true
            useWideViewPort = true
            mixedContentMode =
                WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        }

        webView.addJavascriptInterface(ChartBridge(), "AndroidBridge")
        webView.webViewClient = WebViewClient()

        webView.webChromeClient = object : WebChromeClient() {
            override fun onShowFileChooser(
                webView: WebView?,
                callback: ValueCallback<Array<Uri>>?,
                params: FileChooserParams?
            ): Boolean {
                filePathCallback?.onReceiveValue(null)
                filePathCallback = callback

                val intent = Intent(Intent.ACTION_GET_CONTENT).apply {
                    type = "image/*"
                    addCategory(Intent.CATEGORY_OPENABLE)
                }

                return try {
                    startActivityForResult(
                        Intent.createChooser(intent, "Select chart image"),
                        FILE_CHOOSER_REQUEST
                    )
                    true
                } catch (error: Exception) {
                    filePathCallback?.onReceiveValue(null)
                    filePathCallback = null
                    false
                }
            }
        }

        setContentView(webView)
        webView.loadUrl("file:///android_asset/index.html")
    }

    @Deprecated("Deprecated in Android API")
    override fun onActivityResult(
        requestCode: Int,
        resultCode: Int,
        data: Intent?
    ) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == FILE_CHOOSER_REQUEST) {
            val results =
                WebChromeClient.FileChooserParams.parseResult(resultCode, data)

            filePathCallback?.onReceiveValue(results)
            filePathCallback = null
        }
    }

    @Deprecated("Deprecated in Android API")
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
