package com.selesca.android.pushit.ui;

import com.actionbarsherlock.app.SherlockActivity;
import com.google.android.gcm.GCMRegistrar;
import com.idmission.apps.core.Idm;
import com.idmission.apps.core.ui.DialogUtils;
import com.selesca.android.pushit.R;
import com.selesca.android.pushit.utils.AppSettings;

import android.app.AlertDialog;
import android.os.Bundle;
import android.util.Log;
import android.view.View;


public class LoginActivity extends SherlockActivity {
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		setContentView(R.layout.login_activity);
		Idm.setActivity(this, true);
		
		findViewById(R.id.LoginButton).setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				AlertDialog.Builder builder= new AlertDialog.Builder(LoginActivity.this);
				builder.setTitle("Registration id");
				builder.setMessage("Registration id="+AppSettings.getGCMRegId());
				builder.show();
				
				Log.v("PUSHIT", AppSettings.getGCMRegId());

			}
		});
		
		
		GCMRegistrar.checkDevice(getApplicationContext());
		GCMRegistrar.checkManifest(getApplicationContext());
		String regId = GCMRegistrar.getRegistrationId(getApplicationContext());
		if (regId.equals("")) {
		  GCMRegistrar.register(getApplicationContext(), AppSettings.SENDER_ID);
		} else {
		  Log.v("PUSHIT", "Already registered");
		}
		
		
		
		super.onCreate(savedInstanceState);
	}

}
