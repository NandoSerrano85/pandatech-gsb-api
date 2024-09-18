import { credentials } from '@grpc/grpc-js';
import { UserServiceClient } from './protos/generated/user_grpc_pb';
import {
  RegisterRequest,
  AuthRequest,
  UserRequest,
  UpdateUserRequest
} from './protos/generated/user_pb';

const API_URL = process.env.REACT_APP_API_URL || 'localhost:8000';
const client = new UserServiceClient(API_URL, credentials.createInsecure());

export const registerUser = (userData) => {
    return new Promise((resolve, reject) => {
      const request = new RegisterRequest();
      request.setUsername(userData.username);
      request.setPassword(userData.password);
      request.setEmail(userData.email);
      request.setFirstname(userData.firstname);
      request.setLastname(userData.lastname);
      request.setStoreUrl(userData.store_url);
      request.setApiAccessToken(userData.api_access_token);
  
      client.registerUser(request, (error, response) => {
        if (error) {
          reject(error);
        } else {
          resolve({
            success: response.getSuccess(),
            message: response.getMessage(),
            userId: response.getUserId()
          });
        }
      });
    });
  };
  
  export const authenticateUser = (credentials) => {
    return new Promise((resolve, reject) => {
      const request = new AuthRequest();
      request.setUsername(credentials.username);
      request.setPassword(credentials.password);
  
      client.authenticateUser(request, (error, response) => {
        if (error) {
          reject(error);
        } else {
          resolve({
            success: response.getSuccess(),
            message: response.getMessage(),
            token: response.getToken()
          });
        }
      });
    });
  };
  
  export const getUser = (userId) => {
    return new Promise((resolve, reject) => {
      const request = new UserRequest();
      request.setId(userId);
  
      client.getUser(request, (error, response) => {
        if (error) {
          reject(error);
        } else {
          resolve({
            id: response.getId(),
            username: response.getUsername(),
            firstname: response.getFirstname(),
            lastname: response.getLastname(),
            email: response.getEmail(),
            storeUrl: response.getStoreUrl(),
            apiKey: response.getApiKey(),
            apiAccessToken: response.getApiAccessToken(),
            apiVersion: response.getApiVersion()
          });
        }
      });
    });
  };
  
  export const updateUser = (userData) => {
    return new Promise((resolve, reject) => {
      const request = new UpdateUserRequest();
      request.setId(userData.id);
      request.setFirstname(userData.firstname);
      request.setLastname(userData.lastname);
      request.setEmail(userData.email);
      request.setStoreUrl(userData.store_url);
      request.setApiAccessToken(userData.api_access_token);
  
      client.updateUser(request, (error, response) => {
        if (error) {
          reject(error);
        } else {
          const updatedUser = response.getUpdatedUser();
          resolve({
            success: response.getSuccess(),
            message: response.getMessage(),
            updatedUser: {
              id: updatedUser.getId(),
              username: updatedUser.getUsername(),
              firstname: updatedUser.getFirstname(),
              lastname: updatedUser.getLastname(),
              email: updatedUser.getEmail(),
              storeUrl: updatedUser.getStoreUrl(),
              apiKey: updatedUser.getApiKey(),
              apiAccessToken: updatedUser.getApiAccessToken(),
              apiVersion: updatedUser.getApiVersion()
            }
          });
        }
      });
    });
  };