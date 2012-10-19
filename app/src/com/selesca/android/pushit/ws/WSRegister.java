package com.selesca.android.pushit.ws;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.HttpConnectionParams;

import com.idmission.apps.core.Idm;
import com.selesca.android.pushit.utils.AppSettings;


import android.os.AsyncTask;
import android.os.Build;
import android.provider.Settings.Secure;
import android.util.Log;

@SuppressWarnings("rawtypes")
public class WSRegister extends AsyncTask {

	public WSRegister(String username, String password, String regId) {
		this.username = username;
		this.password = password;
		this.regId = regId;
	}

	public String getStatusMessage() {
		return statusMessage;
	}

	public int getStatusCode() {
		return statusCode;
	}
	
	public void setAsyncTaskListener(AsyncTaskListener asyncTaskListener) {
		this.asyncTaskListener = asyncTaskListener;
	}
	
	@Override
	protected Object doInBackground(Object... arg0) {
		
		String android_id = Secure.getString(Idm.getContext().getContentResolver(),
                Secure.ANDROID_ID); 
		
		HttpClient httpClient = new DefaultHttpClient();
		HttpConnectionParams.setConnectionTimeout(httpClient.getParams(), TIMEOUT_MS);
		HttpConnectionParams.setSoTimeout(httpClient.getParams(), TIMEOUT_MS);
		HttpPost httpPost = new HttpPost(url);  
		List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();  
		nameValuePairs.add(new BasicNameValuePair("username", username));  
		nameValuePairs.add(new BasicNameValuePair("password", password)); 
		nameValuePairs.add(new BasicNameValuePair("device_model", Build.MODEL)); 
		nameValuePairs.add(new BasicNameValuePair("device_oem", Build.MANUFACTURER)); 
		nameValuePairs.add(new BasicNameValuePair("android_id", android_id)); 
		nameValuePairs.add(new BasicNameValuePair("gcm_regid", AppSettings.getGCMRegId())); 
		
		// etc...
		try {
			httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
			HttpResponse response = httpClient.execute(httpPost);
			statusCode = response.getStatusLine().getStatusCode();
			statusMessage = response.getStatusLine().getReasonPhrase();
			Log.i(TAG, "statusResponse: "+response.getStatusLine());
			
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} 
		catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return null;
	}
	
	@SuppressWarnings("unchecked")
	@Override
	protected void onPostExecute(Object result) {
		if(asyncTaskListener != null) {
			asyncTaskListener.onFinished(this);
		}
		
		super.onPostExecute(result);
	}

	
	//Private STUFF
	private static final int TIMEOUT_MS = 20000;
	private static final String  url = AppSettings.BASE_URL + "/api/register";
	
	private String username;
	private String password;
	private String regId;
	private int statusCode;
	private String statusMessage;

	private AsyncTaskListener asyncTaskListener;
	
	private static final String TAG = "PUSHIT: "+ WSRegister.class.getSimpleName() + ": ";
}
