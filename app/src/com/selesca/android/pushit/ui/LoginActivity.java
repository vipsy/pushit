package com.selesca.android.pushit.ui;

import com.google.android.gcm.GCMRegistrar;
import com.idmission.apps.core.Idm;
import com.idmission.apps.core.StringUtilHelper;
import com.idmission.apps.core.ui.BaseActivity;
import com.selesca.android.pushit.R;
import com.selesca.android.pushit.utils.AppSettings;
import com.selesca.android.pushit.ws.AsyncTaskListener;
import com.selesca.android.pushit.ws.WSLogin;
import com.selesca.android.pushit.ws.WSRegister;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;


public class LoginActivity extends BaseActivity implements AsyncTaskListener {
	
	private String username = "";
	private String password = "";
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		setContentView(R.layout.login_activity);
		Idm.setActivity(this, true);
		
		findViewById(R.id.LoginButton).setOnClickListener(new View.OnClickListener() {
			
			@SuppressWarnings("unchecked")
			@Override
			public void onClick(View v) {
//				AlertDialog.Builder builder= new AlertDialog.Builder(LoginActivity.this);
//				builder.setTitle("Registration id");
//				builder.setMessage("Registration id="+AppSettings.getGCMRegId());
//				builder.show();
//				
//				Log.v("PUSHIT", AppSettings.getGCMRegId());
				username = ((EditText)findViewById(R.id.login)).getEditableText().toString();
				password = ((EditText)findViewById(R.id.Password)).getEditableText().toString();
				
				if( !StringUtilHelper.isEmpty(username) && !StringUtilHelper.isEmpty(password) ) {
					WSLogin wsLogin = new WSLogin(username, password);
					wsLogin.setAsyncTaskListener(LoginActivity.this);
					wsLogin.execute();
				}
				
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

	@Override
	public void onFinished(AsyncTask asyncTask) {
		
		if( asyncTask!=null && asyncTask instanceof WSLogin) {
			WSLogin wsLogin = (WSLogin) asyncTask;
			if(wsLogin.getStatusCode() == 200) {
				Toast.makeText(this, "Login successful, you device will be registered soon", 
						Toast.LENGTH_SHORT).show();
				
				AppSettings.setUsername(username);
				AppSettings.setPassword(password);
				new WSRegister(AppSettings.getUsername(), AppSettings.getPassword(), AppSettings.getGCMRegId() ).execute();

				this.finish();
			}else {
				Toast.makeText(this, "Login failed: Response="+wsLogin.getStatusMessage(), 
						Toast.LENGTH_SHORT).show();
			}
		}
		
	}
	
/****************************************************************************************/

	

}
