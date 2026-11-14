package com.alphatradingai

import android.app.Activity
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.Bundle
import android.util.Base64
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import java.io.ByteArrayOutputStream

class MainActivity : Activity() {

    private lateinit var webView: WebView

    inner class ChartBridge {
        @JavascriptInterface
        fun captureChart() {
            runOnUiThread {
                if (!::webView.isInitialized ||
                    webView.width <= 0 || webView.height <= 0
                ) return@runOnUiThread

                val bitmap = Bitmap.createBitmap(
                    webView.width,
                    webView.height,
                    Bitmap.Config.ARGB_8888
                )

                webView.draw(Canvas(bitmap))

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
            mixedContentMode = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        }

        webView.addJavascriptInterface(ChartBridge(), "AndroidBridge")
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()

        setContentView(webView)
        webView.loadUrl("file:///android_asset/index.html")
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
