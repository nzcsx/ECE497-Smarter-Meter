import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState, useEffect } from 'react';
import {
    StyleSheet,
    View,
    Text,
    Alert,
    TextInput,
} from 'react-native';
import CustomButton from '../Utils/CustomButton';
import GlobalStyle from '../Styles/TextStyle';
import SQLite from 'react-native-sqlite-storage';

import {useSelector, useDispatch} from 'react-redux';
import {setName, setPassword} from '../Redux/actions';
import { createStackNavigator } from 'react-navigation-stack';

const db = SQLite.openDatabase(
    {
        name: 'MainDB',
        location: 'default',
    },
    () => { },
    error => { console.log(error) }
);

export default function InfoScreen({ navigation, route }) {

    const {name,password} = useSelector(state=>state.userReducer);
    const dispatch = useDispatch();

    useEffect(() => {
        getData();
    }, []);

    const getData = () => {
        try {
            db.transaction((tx) => {
                tx.executeSql(
                    "SELECT Name, Password FROM Users",
                    [],
                    (tx, results) => {
                        var len = results.rows.length;
                        if (len > 0) {
                            var userName = results.rows.item(0).Name;
                            var userPassword = results.rows.item(0).Password;
                            dispatch(setName(userName));
                            dispatch(setName(userPassword));
                        }
                    }
                )
            })
        } catch (error) {
            console.log(error);
        }
    }

    // const updateData = async () => {
    //     if (name.length == 0) {
    //         Alert.alert('Warning!', 'Please write your data.')
    //     } else {
    //         try {
    //             db.transaction((tx) => {
    //                 tx.executeSql(
    //                     "UPDATE Users SET Name=?",
    //                     [name],
    //                     () => { Alert.alert('Success!', 'Your data has been updated.') },
    //                     error => { console.log(error) }
    //                 )
    //             })
    //         } catch (error) {
    //             console.log(error);
    //         }
    //     }
    // }

    const removeData = async () => {
        try {
            // await AsyncStorage.clear();
            db.transaction((tx) => {
                tx.executeSql(
                    "DELETE FROM Users",
                    [],
                    () => { navigation.navigate('Login') },
                    error => { console.log(error) }
                )
            })
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <View style={styles.body}>
            <Text style={[
                styles.text
            ]}>
                Welcome Dear {name} !
            </Text>
            <Text style={[
                styles.text
            ]}>
                Your Password is {password}
            </Text>
            
            {/* <TextInput
                style={styles.input}
                placeholder='Enter your name'
                value={name}
                onChangeText={(value) => dispatch(setName(name))}
            />
            <CustomButton
                title='Update'
                color='#ff7f00'
                onPressFunction={updateData}
            /> */}
            <CustomButton
                title='Logout'
                color='#f40100'
                //onPressFunction={navigation.navigate('Settings')}
            />
        </View>
    )
}

const styles = StyleSheet.create({
    body: {
        flex: 1,
        alignItems: 'center',
    },
    text: {
        fontSize: 20,
        margin: 10,
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

 
