import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState, useEffect } from 'react';
import {
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

export default function Home({ navigation, route }) {


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
                source={require('../../assets/report/local_report.jpg')}
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
                        
                    /> 
                </View>
                <View style={styles.buttonStyle}>
                    <CustomButton
                        title='Spatial'
                        color='#1338ee'
                        
                    /> 
                </View>
            </View>
            <View style={{ flexDirection:"row" }}>
                <View style={styles.buttonStyle}>
                    <CustomButton
                        title='My Bill'
                        color='#13adbe'
                        
                    /> 
                </View>
                <View style={styles.buttonStyle}>
                    <CustomButton
                        title='My report'
                        color='#13afee'
                        
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