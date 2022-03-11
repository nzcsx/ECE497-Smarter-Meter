/**
  Smart Meter Application - University of Toronto
  Member: Jiaping Lin
  Member: 

 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Setting from './FrontEnd/Screens/SettingScreen';
import Login from './FrontEnd/Screens/LoginScreen';
import Home from './FrontEnd/Screens/HomeScreen';
import { Provider } from 'react-redux';
import { Store } from './FrontEnd/Redux/store';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function NestedHome() {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Home"
        component={Home}
      />
      <Tab.Screen
        name="Setting"
        component={Setting}
      />
    </Tab.Navigator>
  );
}

function App() {
  return (
    <Provider store = {Store}>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="Login"
          screenOptions={{
            headerTitleAlign: 'center',
            headerStyle: {
              backgroundColor: '#0080ff'
            },
            headerTintColor: '#ffffff',
            headerTitleStyle: {
              fontSize: 25,
              fontWeight: 'bold'
            }
          }}
        >
          <Stack.Screen
            name="Login"
            component={Login}
            options={{
              headerShown: false,
            }}
          />

          <Stack.Screen
            name="NestedHome"
            component={NestedHome}
            options={{
              headerShown: false,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </Provider>
  )
}

export default App;