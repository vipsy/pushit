package com.selesca.android.pushit.utils;


public class AppSettings extends com.idmission.apps.core.AppSettings {
	
	public static final String SENDER_ID = "254929753609"; 
	public static final String BASE_URL = "http://pushit-selesca.rhcloud.com";
	
	private static String  GCM_REG_ID = "GCM_REG_ID";
	private static String  USERNAME = "USERNAME";
	private static String  PASSWORD = "PASSWORD";
	
	public static void setGCMRegId(String regId){
		AppSettings.setString(GCM_REG_ID, regId);
	}
	
	public static String getGCMRegId() {
		return AppSettings.getString(GCM_REG_ID, "");
	}

	public static void setUsername(String username){
		AppSettings.setString(USERNAME, username);
	}
	
	public static String getUsername() {
		return AppSettings.getString(USERNAME, "");
	}
	
	public static void setPassword(String password){
		AppSettings.setString(PASSWORD, password);
	}
	
	public static String getPassword() {
		return AppSettings.getString(PASSWORD, "");
	}
}
