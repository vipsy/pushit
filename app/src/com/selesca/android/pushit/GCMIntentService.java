package com.selesca.android.pushit;

import com.google.android.gcm.GCMBaseIntentService;
import com.idmission.apps.core.Idm;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.util.Log;
import android.widget.Toast;

import com.selesca.android.pushit.utils.AppSettings;
import com.selesca.android.pushit.ws.WSRegister;

public class GCMIntentService extends GCMBaseIntentService {

    public GCMIntentService() {
		super(AppSettings.SENDER_ID);
	}
	
	@Override
	protected void onMessage(Context context, Intent intent) {
		//Idm.setContext(context);
		String key1 = intent.getExtras().getString("key1");
			
		
		Log.i("PUSHIT", "GCM Message: "+key1);
		Intent smsIntent = new Intent(Intent.ACTION_VIEW);         
		smsIntent.setData(Uri.parse("sms:"));
		smsIntent.putExtra("sms_body", key1 ); 
		smsIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
		context.startActivity(smsIntent);
		
		//Toast.makeText(getApplicationContext(), intent.getExtas().getString("data"), Toast.LENGTH_SHORT).show();
	}

	
	@Override
	protected void onRegistered(Context context, String regId) {
		Idm.setContext(context);
		Log.i("PUSHIT", "onRegistered:  regId= "+regId);
		AppSettings.setGCMRegId(regId);
		new WSRegister(AppSettings.getUsername(), AppSettings.getPassword(), AppSettings.getGCMRegId() ).execute();
	}

	
	@Override
	protected void onUnregistered(Context context, String regId) {
		Idm.setContext(context);
		AppSettings.setGCMRegId("");
		new WSRegister(AppSettings.getUsername(), AppSettings.getPassword(), "").execute();
	}
	

	@Override
	protected void onError(Context context, String errorId) {
		Idm.setContext(context);
		// TODO Auto-generated method stub
		
	}

	@Override
	protected boolean onRecoverableError(Context context, String errorId) {
		// TODO Auto-generated method stub
		Idm.setContext(context);
		return super.onRecoverableError(context, errorId);
	}
	
}
