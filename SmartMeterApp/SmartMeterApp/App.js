/**
  Smart Meter Application - University of Toronto
  Member: Jiaping Lin
  Member: 

 */

import React from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
// import { createSwitchNavigator} from '@react-navigation/core/src/navigators';
import SettingScreen from './FrontEnd/Screens/SettingScreen';
import Login from './FrontEnd/Screens/LoginScreen';
import Home from './FrontEnd/Screens/HomeScreen';
import InfoScreen from './FrontEnd/Screens/InfoScreen';
import SurveyScreen from './FrontEnd/Screens/SurveyScreen';
import RegisterScreen from './FrontEnd/Screens/RegisterScreen';
import ResetScreen from './FrontEnd/Screens/ResetScreen';
import ReportScreen from './FrontEnd/Screens/ReportScreen';
import TemporalScreen from './FrontEnd/Screens/TemporalScreen';
import SpatialScreen from './FrontEnd/Screens/SpatialScreen';
import billScreen from './FrontEnd/Screens/billScreen';
import { Provider } from 'react-redux';
import { Store } from './FrontEnd/Redux/store';


const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();
// const Pile = createSwitchNavigator();

function NestedSettings() {
  return (
    <Stack.Navigator
          initialRouteName="NestedSettings"
          component={SettingScreen}
          screenOptions={{
            headerShown: false,
            header: null,
          }}
        >
        <Tab.Screen
        name="NestedSettings"
        headerShown="false"
        component={SettingScreen}
      />
      <Stack.Screen
        name="InfoScreen"
        screenOptions={{
          headerShown: false,
          header: null,
        }}
        component={InfoScreen}
      />
      <Stack.Screen
        name="SurveyScreen"
        headerShown="false"
        component={SurveyScreen}
      />
      <Stack.Screen
            name="ResetScreen"
            component={ResetScreen}
            options={{
              headerShown: false,
              header: null,
            }}
          />
      
    </Stack.Navigator>
  );
}

function NestedReport(){
  return (
    <Stack.Navigator
          initialRouteName="NestedReport"
          component={Home}
          screenOptions={{
            headerShown: false,
            header: null,
          }}
        >
        
        <Tab.Screen
        name="NestedReport"
        headerShown="false"
        component={Home}
      />
      <Stack.Screen
        name="ReportScreen"
        screenOptions={{
          headerShown: false,
          header: null,
        }}
        component={ReportScreen}
      />

      <Stack.Screen
        name="TemporalScreen"
        screenOptions={{
          headerShown: false,
          header: null,
        }}
        component={TemporalScreen}
      />

      <Stack.Screen
        name="SpatialScreen"
        screenOptions={{
          headerShown: false,
          header: null,
        }}
        component={SpatialScreen}
      />

    <Stack.Screen
        name="billScreen"
        screenOptions={{
          headerShown: false,
          header: null,
        }}
        component={billScreen}
      />
    
      
    </Stack.Navigator>
  );
}

function NestedHome() {
  return (
    <Tab.Navigator >

      <Tab.Screen
        name="Home"
        screenOptions={{
          headerShown: false,
          header: null,
        }}
        component={NestedReport}
      />
      <Tab.Screen
        name="Settings"
        headerShown="false"
        component={NestedSettings}
      />
      {/* <Stack.Screen
        name="InfoScreen"
        screenOptions={{
          headerShown: false,
          header: null,
        }}
        component={InfoScreen}
      />
      <Stack.Screen
        name="SurveyScreen"
        headerShown="false"
        component={SurveyScreen}
      /> */}
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
            headerShown: false,
            header: null,
          }}
        >
          <Stack.Screen
            name="Login"
            component={Login}
            options={{
              headerShown: false,
              header: null,
            }}
          />

          <Stack.Screen
            name="NestedHome"
            component={NestedHome}
            options={{
              headerShown: false,
              header: null,
            }}
          />

          <Stack.Screen
            name="RegisterScreen"
            component={RegisterScreen}
            options={{
              headerShown: false,
              header: null,
            }}
          />

          <Stack.Screen
            name="ResetScreen"
            component={ResetScreen}
            options={{
              headerShown: false,
              header: null,
            }}
          />

        </Stack.Navigator>
      </NavigationContainer>
    </Provider>
  )
}

export default App;