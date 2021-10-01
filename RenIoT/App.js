import * as React from 'react'
import { View, StyleSheet } from 'react-native'
import {NavigationContainer} from '@react-navigation/native'
import {createStackNavigator} from '@react-navigation/stack'
import HomeScreen from './components/HomeScreen';
import LoginScreen from '../RenIoT/components/LoginScreen';
import SignUpScreen from './components/SignUpScreen';
import BoxSignUpScreen from './components/BoxSignUpScreen';
import BoxLoginScreen from './components/BoxLoginScreen';
import ForgotPasswordScreen from './components/ForgotPasswordScreen';
import OtpValidationScreen from './components/OtpValidationScreen'
import RenIoT from './components/RenIoT';

const Stack = createStackNavigator();

export default class App extends React.Component{
  render(){
    return(
      <View style= {styles.container}>
        <NavigationContainer>
          <Stack.Navigator initialRouteName="Home">
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="SignUp" component={SignUpScreen} />
            <Stack.Screen name="RenIoT" component={RenIoT} />
            <Stack.Screen name="BoxSignUp" component={BoxSignUpScreen} />
            <Stack.Screen name="BoxLogin" component={BoxLoginScreen} />
            <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} />
            <Stack.Screen name="OtpValidationScreen" component={OtpValidationScreen} />
          </Stack.Navigator>
        </NavigationContainer>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
      flex: 1,
      backgroundColor: '#FFF'
  }
})
