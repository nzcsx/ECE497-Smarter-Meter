import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState, useEffect, Component } from 'react';
import {
    AppRegistry,
    RefreshControl,
    StyleSheet,
    View,
    Text,
    Alert,
    TextInput,
    Image,
} from 'react-native';
import CustomButton from '../Utils/CustomButton';
import GlobalStyle from '../Styles/TextStyle';
import SQLite from 'react-native-sqlite-storage';

'use strict';
import SettingsList from 'react-native-settings-list';
import {useSelector, useDispatch} from 'react-redux';
import {setName, setPassword} from '../Redux/actions';
import { createStackNavigator } from 'react-navigation-stack';
import { State } from 'react-native-gesture-handler';
import {userReducer} from '../Redux/reducers'


 class Home extends Component {
    constructor(props){
        super(props);
        next_source = require("../../assets/report/local_report.jpg");
        this.state = {img_source: next_source};
        
    }

    request_report_temporal = () =>
    {
        fetch("http://127.0.0.1:5000/report", {method: "POST",
            body: "temporal", 
            header: {
                'Content-Type': 'application/json'
                } // <-- Post parameters        
        })
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson);
        //    this.setState({
        //       data: responseJson
        //    })
        })
        .catch((error) => {
            console.error(error);
        });
        require_img = require("../../assets/report/temporal1.png")
        this.setState({img_source: require_img});
        
    }

    request_report_spatial = () =>
    {
        fetch("http://127.0.0.1:5000/report", {method: "POST",
            body: "spatial", 
            header: {
                'Content-Type': 'application/json'
                } // <-- Post parameters        
        })
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson);
        //    this.setState({
        //       data: responseJson
        //    })
        })
        .catch((error) => {
            console.error(error);
        });
        require_img = require("../../assets/report/spatial1.png")
        this.setState({img_source: require_img});
        
    }

    request_report_bill = () =>
    {
        fetch("http://127.0.0.1:5000/report", {method: "POST",
            body: "bill", 
            header: {
                'Content-Type': 'application/json'
                } // <-- Post parameters        
        })
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson);
        //    this.setState({
        //       data: responseJson
        //    })
        })
        .catch((error) => {
            console.error(error);
        });
        require_img = require("../../assets/report/bill1.png")
        this.setState({img_source: require_img});
        
    }

    render() {
        var bgColor = '#83cfe3';
        // const {name,password} = useSelector(state=>state.userReducer);
        // const dispatch = useDispatch();

        return (
            
            <View style={styles.body}>
                <View style = {styles.backgroundContainer}>
                <Image
                    style={styles.logo_curve}
                    source={require('../../assets/icon/curve.png')}
                />
            </View>
                <Text style={[
                    styles.text
                ]}>
                    Your consumption:
                </Text>
                <Image
                    style={styles.logo}
                    source={this.state.img_source}
                />
                <Text style={[
                    styles.text
                ]}>
                    Report Selection
                </Text>
                <View style={{ flexDirection:"row" }}>
                    <View style={styles.buttonStyle}>
                        <CustomButton
                            title='Temporal'
                            color='#133bbe'
                            //onPressFunction={this.request_report_temporal}
                            onPressFunction={() => { this.props.navigation.navigate('TemporalScreen') }}
                        /> 
                    </View>
                    <View style={styles.buttonStyle}>
                        <CustomButton
                            title='Spatial'
                            color='#1338ee'
                            //onPressFunction={this.request_report_spatial}
                            onPressFunction = {() => { this.props.navigation.navigate('SpatialScreen') }}
                        /> 
                    </View>
                </View>
                <View style={{ flexDirection:"row" }}>
                    <View style={styles.buttonStyle}>
                        <CustomButton
                            title='My Bill'
                            color='#13adbe'
                            //onPressFunction={this.request_report_bill}
                            onPressFunction = {() => { this.props.navigation.navigate('billScreen') }}
                        /> 
                    </View>
                    <View style={styles.buttonStyle}>
                        <CustomButton
                            title='My report'
                            color='#13afee'
                            onPressFunction={() => { this.props.navigation.navigate('ReportScreen') }}
                        /> 
                    </View>
                </View>
            </View>
        );
        }

  }


// export default function Home({ navigation, route }) {
//     // need to specify the min/max date of readings
//     source_img = "../../assets/report/local_report.jpg"
//     var require_img = require("../../assets/report/local_report.jpg")
//     const [refreshing, setRefreshing] = React.useState(false);

//     const wait = (timeout) => {
//         return new Promise(resolve => setTimeout(resolve, timeout));
//     }

//     const request_report = () => 
//     {

//         fetch("http://127.0.0.1:5000/report", {method: "POST",
//             body: "report_type", 
//             header: {
//                 'Content-Type': 'application/json'
//               } // <-- Post parameters        
//         })
//         .then((response) => response.json())
//         .then((responseJson) => {
//            console.log(responseJson);
//         //    this.setState({
//         //       data: responseJson
//         //    })
//         })
//         .catch((error) => {
//            console.error(error);
//         });
//         source_img = '../../assets/report/temporal1.png'
//         require_img = require('../../assets/report/temporal1.png')
//         console.log(source_img)
//         // setRefreshing(true);
//         // wait(2000).then(() => setRefreshing(false));
//         navigation.navigate('NestedHome', { screen: 'Settings' });
        
//    }



//     return (
        
//         <View style={styles.body}>
//             <View style = {styles.backgroundContainer}>
//             <Image
//                 style={styles.logo_curve}
//                 source={require('../../assets/icon/curve.png')}
//             />
//         </View>
//             <Text style={[
//                 styles.text
//             ]}>
//                 Your consumption:
//             </Text>
//             <Image
//                 style={styles.logo}
//                 source={require_img}
//             />
//             <Text style={[
//                 styles.text
//             ]}>
//                 Report Selection
//             </Text>
//             <View style={{ flexDirection:"row" }}>
//                 <View style={styles.buttonStyle}>
//                     <CustomButton
//                         title='Temporal'
//                         color='#133bbe'
//                         onPressFunction={request_report}
//                     /> 
//                 </View>
//                 <View style={styles.buttonStyle}>
//                     <CustomButton
//                         title='Spatial'
//                         color='#1338ee'
                        
//                     /> 
//                 </View>
//             </View>
//             <View style={{ flexDirection:"row" }}>
//                 <View style={styles.buttonStyle}>
//                     <CustomButton
//                         title='My Bill'
//                         color='#13adbe'
                        
//                     /> 
//                 </View>
//                 <View style={styles.buttonStyle}>
//                     <CustomButton
//                         title='My report'
//                         color='#13afee'
                        
//                     /> 
//                 </View>
//             </View>
//         </View>
//     )
// }

const styles = StyleSheet.create({
    backgroundContainer: {
        position: 'absolute',
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
      },
    body: {
        flex: 1,
        alignItems: 'center',
    },
    text: {
        fontSize: 40,
        margin: 10,
    },
    logo: {
        width: 450,
        height: 300,
        margin: 20,
    },
    input: {
        width: 300,
        borderWidth: 1,
        borderColor: '#555',
        borderRadius: 10,
        backgroundColor: '#ffffff',
        textAlign: 'center',
        fontSize: 20,
        marginTop: 130,
        marginBottom: 10,
    }
})

module.exports = Home;