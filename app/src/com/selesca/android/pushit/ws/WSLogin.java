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

import android.os.AsyncTask;

public class WSLogin extends AsyncTask {
	
	private static final int TIMEOUT_MS = 20000;
	private static final String  url = "192.168.56.1:8000/login";

	@Override
	protected Object doInBackground(Object... arg0) {
		
		HttpClient httpClient = new DefaultHttpClient();
		HttpConnectionParams.setConnectionTimeout(httpClient.getParams(), TIMEOUT_MS);
		HttpConnectionParams.setSoTimeout(httpClient.getParams(), TIMEOUT_MS);
		HttpPost httpPost = new HttpPost(url);  
		List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();  
		nameValuePairs.add(new BasicNameValuePair("name1", "value1"));  
		nameValuePairs.add(new BasicNameValuePair("name2", "value2")); 
		nameValuePairs.add(new BasicNameValuePair("name3", "value3"));   
		// etc...
		try {
			httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
			HttpResponse response = httpClient.execute(httpPost);
			
			
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

}
