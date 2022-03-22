import React, { useState, useEffect } from 'react';
import {
    View,
    StyleSheet,
    Image,
    Text,
    TextInput,
    Alert,
} from 'react-native';
import CustomButton from '../Utils/CustomButton';
// import AsyncStorage from '@react-native-async-storage/async-storage';
import SQLite from 'react-native-sqlite-storage';
import {useSelector, useDispatch} from 'react-redux';
import {setName, setPassword} from '../Redux/actions';

const db = SQLite.openDatabase(
    {
        name: 'MainDB',
        location: 'default',
    },
    () => { },
    error => { console.log(error) }
);

export default function Login({ navigation }) {

    const {name,password} = useSelector(state=>state.userReducer);
    const dispatch = useDispatch();
    verification = '';

    useEffect(() => {
        createTable();
        getData();
    }, []);

    const check_login = () => {
        const info = 'uname='+name+'&password='+password;
        console.log(info);

        fetch("http://127.0.0.1:5000/login", {method: "POST",
            body: info, 
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
            verification = responseJson.valid;

            if (verification == "True")
            {
                navigation.navigate('NestedHome', { screen: 'Home' });
            }
            else
            {
                Alert.alert("Unable to find user name or password in database.");
                navigation.navigate('Login');
            }
        })
        .catch((error) => {
           console.error(error);
        });
        
   }

   const registerUser = () => {
        navigation.navigate('RegisterScreen');
    }

    const resetUser = () => {
        navigation.navigate('ResetScreen');
    }

    const createTable = () => {
        db.transaction((tx) => {
            tx.executeSql(
                "CREATE TABLE IF NOT EXISTS "
                + "Users "
                + "(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Age INTEGER);"
            )
        })
    }

    const getData = () => {
        try {
            db.transaction((tx) => {
                tx.executeSql(
                    "SELECT Name, Password FROM Users",
                    [],
                    (tx, results) => {
                        var len = results.rows.length;
                        if (len > 0) {
                            navigation.navigate('NestedHome', { screen: 'Home' });
                        }
                    }
                )
            })
        } catch (error) {
            console.log(error);
        }
    }

    const setData = async () => {
        if (name.length == 0 || password.length == 0) {
            Alert.alert('Warning!', 'Please write your data.')
        } else {
            try {
                dispatch(setName(name));
                dispatch(setPassword(password));

                await db.transaction(async (tx) => {

                    await tx.executeSql(
                        "INSERT INTO Users (Name, Password) VALUES (?,?)",
                        [name, password]
                    );
                })
                //navigation.navigate('NestedHome', { screen: 'Home' });
            } catch (error) {
                console.log(error);
            }
        }
    }

    return (
        <View style={styles.body} >
            <View style = {styles.backgroundContainer}>
            <Image
                style={styles.logo_curve}
                source={require('../../assets/icon/curve.png')}
            />
            </View>
            <Text style={styles.text}>
            </Text>

            <Image
                style={styles.logo}
                source={require('../../assets/icon/icon.png')}
            />
            <TextInput
                style={styles.input}
                placeholder='Enter your name'
                onChangeText={(value) => dispatch(setName(value))}
            />
            <TextInput
                style={styles.input}
                placeholder='Enter your password'
                onChangeText={(value) => dispatch(setPassword(value))}
            />
            <CustomButton
                title='Login'
                color='#83cfe3'
                onPressFunction={check_login}
            />
            <View style={{ flexDirection:"row" }}>
                    <View style={styles.buttonStyle}>
                        <CustomButton
                            title='Forget Key'
                            color='#83cfe3'
                            onPressFunction={resetUser}
                        /> 
                    </View>
                    <View style={styles.buttonStyle}>
                        <CustomButton
                            title='Register'
                            color='#83cfe3'
                            onPressFunction={registerUser}
                        /> 
                    </View>
            </View>
        </View>
    )
}

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
        backgroundColor: '#eeeeee',
    },
    logo: {
        resizeMode: "cover",
        width: 130,
        height: 130,
        margin: 20,
    },
    logo_curve: {
        resizeMode: "cover",
        width: 420,
        height: 420,
        margin: 0,
    },
    text: {
        fontSize: 30,
        color: '#83cfe3',
        marginBottom: 65,
    },
    input: {
        width: 300,
        borderWidth: 1,
        borderColor: '#555',
        borderRadius: 10,
        backgroundColor: '#f9f9f9',
        textAlign: 'center',
        fontSize: 20,
        marginBottom: 10,
    }
})