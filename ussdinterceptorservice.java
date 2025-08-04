package org.zulu.sentinel;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.widget.Toast;

public class USSDInterceptorService extends AccessibilityService {

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event == null || event.getText() == null) return;

        for (CharSequence text : event.getText()) {
            if (text != null && text.toString().startsWith("*#")) {
                Toast.makeText(this, "SentinelIT: USSD code blocked", Toast.LENGTH_SHORT).show();

                // Optional: Additional logic to block the request or alert the app
                // You can try to use performGlobalAction(GLOBAL_ACTION_BACK) to simulate back press
            }
        }
    }

    @Override
    public void onInterrupt() {
        // Called when the system wants to interrupt the accessibility feedback
    }

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        Toast.makeText(this, "SentinelIT: USSD Interceptor Active", Toast.LENGTH_SHORT).show();
    }
}
