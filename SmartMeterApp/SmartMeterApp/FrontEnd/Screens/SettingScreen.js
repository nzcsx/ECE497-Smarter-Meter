import AsyncStorage from '@react-native-async-storage/async-storage';

import CustomButton from '../Utils/CustomButton';
import GlobalStyle from '../Styles/TextStyle';
import SQLite from 'react-native-sqlite-storage';
import Login from './LoginScreen'
import InfoScreen from './InfoScreen'
import SurveyScreen from './InfoScreen'
import Home from './HomeScreen'
// import {useSelector, useDispatch} from 'react-redux';
// import {setName, setPassword} from '../Redux/actions';

const db = SQLite.openDatabase(
    {
        name: 'MainDB',
        location: 'default',
    },
    () => { },
    error => { console.log(error) }
);

'use strict';
import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  Image,
  Alert,
} from 'react-native';

import SettingsList from 'react-native-settings-list';
import {useSelector, useDispatch} from 'react-redux';
import {setName, setPassword} from '../Redux/actions';
import { createStackNavigator } from 'react-navigation-stack';
import { State } from 'react-native-gesture-handler';
import {userReducer} from '../Redux/reducers'

/**
 * realistic iPhone example
 */
 class SettingsScreen extends Component {
    constructor(props){
        super(props);
        next_source = require('../../assets/icon/night.png');
        this.onValueChange = this.onValueChange.bind(this);
        this.handleNameChange = this.handleNameChange.bind(this);
        this.state = {switchValue: false, loggedIn: false, 
            name:this.props.name, password:"",data: '', 
            bkg_colour:"#EFEFF4", bar_colour:'#ffffff', language:'English', img_source: next_source};
        
    }

    componentDidMount = () => {
        fetch('http://127.0.0.1:5000/time', {
           method: 'GET'
        })
        .then((response) => response.json())
        .then((responseJson) => {
           console.log(responseJson);
           this.setState({
              data: responseJson
           })
        })
        .catch((error) => {
           console.error(error);
        });
     }

    render() {
        var bgColor = '#83cfe3';
        // const {name,password} = useSelector(state=>state.userReducer);
        // const dispatch = useDispatch();

        return (
            <View style={{backgroundColor:this.state.bkg_colour,flex:1}}>
            {/* <View style={{borderBottomWidth:1, backgroundColor:'#f7f7f8',borderColor:'#c8c7cc'}}>
                <Text style={{alignSelf:'center',marginTop:30,marginBottom:10,fontWeight:'bold',fontSize:16}}>Settings</Text>
            </View> */}
            <View style={{backgroundColor:this.state.bkg_colour,flex:1}}>
                <SettingsList borderColor='#c8c7cc' defaultItemSize={50}>
                {/* <SettingsList.Header headerStyle={{marginTop:15}}/>
                {this.state.toggleAuthView ?
                    <SettingsList.Item
                    icon={
                        <Image style={styles.imageStyle} source={require('../../assets/icon/head.png')}/>
                    }
                    title='Logged In As...'
                    hasNavArrow={false}
                    />
                    :
                    <SettingsList.Item
                    icon={
                        <Image style={styles.imageStyle} source={require('../../assets/icon/head.png')}/>
                    }
                    isAuth={true}
                    authPropsUser= {{placeholder:this.state.name}}
                    authPropsPW={{placeholder:'Password'}}
                    onPress={() => this.handleNameChange()}
                    />
                } */}
                <SettingsList.Header headerStyle={{marginTop:15}}/>
                <SettingsList.Item
                    icon={
                        <Image style={styles.imageStyle} source={require('../../assets/icon/head.png')}/>
                    }
                    
                    //hasSwitch={true}
                    // switchState={this.state.switchValue}
                    // switchOnValueChange={this.onValueChange}
                    title='User Information'
                    backgroundColor = {this.state.bar_colour}
                    onPress={() => { this.props.navigation.navigate('InfoScreen') }}
                />
                <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={require('../../assets/icon/info.png')}/>}
                    title='Change My Information'
                    titleInfoStyle={styles.titleInfoStyle}
                    backgroundColor = {this.state.bar_colour}
                    onPress={() => { this.props.navigation.navigate('SurveyScreen') }}
                />
                <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={this.state.img_source}/>}
                    title='Night Mode'
                    hasSwitch={true}
                    switchState={this.state.switchValue}
                    switchOnValueChange={this.onValueChange}
                    backgroundColor = {this.state.bar_colour}
                    hasNavArrow={false}
                />
                <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={require('../../assets/icon/password.png')}/>}
                    title='Reset Password'
                    onPress={() => { this.props.navigation.navigate('ResetScreen') }}
                    backgroundColor = {this.state.bar_colour}
                />
                {/* <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={require('../../assets/icon/hotspot.png')}/>}
                    title='Personal Hotspot'
                    titleInfo='Off'
                    titleInfoStyle={styles.titleInfoStyle}
                    backgroundColor = {this.state.bar_colour}
                    onPress={() => Alert.alert('Route To Hotspot Page')}
                /> */}
                <SettingsList.Header headerStyle={{marginTop:15}}/>
                <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={require('../../assets/icon/notifications.png')}/>}
                    title='Notifications'
                    backgroundColor = {this.state.bar_colour}
                    onPress={() => Alert.alert('Route To Notifications Page')}
                />
                <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={require('../../assets/icon/language.png')}/>}
                    title='Language'
                    titleInfo={this.state.language}
                    titleInfoStyle={styles.titleInfoStyle}
                    backgroundColor = {this.state.bar_colour}
                    onPress={() => Alert.alert('Route To Control Center Page')}
                />
                <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={require('../../assets/icon/issue.png')}/>}
                    title='Report Issues'
                    backgroundColor = {this.state.bar_colour}
                    onPress={() => Alert.alert('Route To Do Not Disturb Page')}
                />
                <SettingsList.Header headerStyle={{marginTop:15}}/>

                <SettingsList.Item
                    icon={<Image style={styles.imageStyle} source={require('../../assets/icon/logout.png')}/>}
                    title='Log Out'
                    backgroundColor = {this.state.bar_colour}
                    arrowStyle={{tintColor:'#dd1100'}}
                    onPress={() => { this.props.navigation.navigate('Login') }}
                />
                </SettingsList>

                <View style={{justifyContent: "center", alignItems: "center", flex: 1}}>
                    <Text style={{backgroundColor:this.state.bkg_colour,flex:1}}>
                        Visited Time: {this.state.data.time}
                    </Text>
                </View>
                
            </View>
            </View>
            );
        }
        toggleAuthView() {
            this.setState({toggleAuthView: !this.state.toggleAuthView});
        }
        onValueChange(value){
            this.setState({switchValue: value});
            if (value == 1)
            {
                this.setState({bkg_colour: '#181818'});
                this.setState({bar_colour:'#7d7d7d'});
                next_source = require('../../assets/icon/day.png');
                this.setState({img_source: next_source});
            }
            else
            {
                this.setState({bkg_colour: '#EFEFF4'});
                this.setState({bar_colour:'#ffffff'});
                next_source = require('../../assets/icon/night.png');
                this.setState({img_source: next_source});
            }
            
        }
        
        handleNameChange(name) {
          this.setState({ name });
        }

  }

 
 const styles = StyleSheet.create({
   imageStyle:{
     marginLeft:15,
     alignSelf:'center',
     height:30,
     width:30
   },
   titleInfoStyle:{
     fontSize:16,
     color: '#8e8e93'
   }
 });
const colors = {
    white: "#FFFFFF",
    monza: "#C70039",
    switchEnabled: "#C70039",
    switchDisabled: "#efeff3",
    blueGem: "#27139A",
    black: "#111111"
};

 module.exports = SettingsScreen;