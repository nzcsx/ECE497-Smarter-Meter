import React from 'react'
import {
  View,
  Button,
  TextInput,
  StyleSheet,
  Image,
  Alert,
  Text, ScrollView
} from 'react-native'

export default class ReportScreen extends React.Component {
    state = {
        username: '', password: '', family: '', reset_Q: '', reset_A: '', 
        confirm_password: '', start_date:'', end_date: '', report: '',
    }
    onChangeText = (key, val) => {
        this.setState({ [key]: val })
    }
    GetReport = async () => {
        //const { username, password, family, reset_Q, reset_A, confirm_password } = this.state

        info = "date1="+this.state.start_date+"&date2="+this.state.end_date;
        console.log(info);

        fetch("http://127.0.0.1:5000/getReport", {method: "POST",
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
            verification = responseJson.report;
            this.setState({report: responseJson.report});

            

        })
        .catch((error) => {
           console.error(error);
        });
    }
    
    render() {
        return (
            
        <View style={styles.container}>

            <Image
                style={styles.logo}
                source={require('../../assets/icon/power_2.png')}
            />
            <Text style={[styles.text]}>
                    Report Center
            </Text>

            <View style={{ flexDirection:"row" }}>
                <Text style={[styles.text2]}>
                        From: 
                </Text>
                <TextInput
                    style={styles.input}
                    placeholder='Start Date (YYYY-MM-DD)'
                    autoCapitalize="none"
                    placeholderTextColor='white'
                    onChangeText={val => this.onChangeText('start_date', val)}
                />
            </View>

            <View style={{ flexDirection:"row" }}>
                <Text style={[styles.text2]}>
                        To  :   
                </Text>
                <TextInput
                    style={styles.input}
                    placeholder='End Date (YYYY-MM-DD)'
                    autoCapitalize="none"
                    placeholderTextColor='white'
                    onChangeText={val => this.onChangeText('end_date', val)}
                />
            </View>

            <ScrollView style={styles.scrollView}>
                <Text style={styles.text3}>
                    {this.state.report}
                </Text>
            </ScrollView>

            {/* <Text style={[styles.text3]}>
                    {this.state.report}
            </Text> */}
           
            <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>
                <Button
                title='Get Report'
                onPress={this.GetReport}
                />

                <Button
                title='Home'
                onPress={() => {this.props.navigation.navigate('NestedReport') }}
                />
            </View>
        </View>
        )
    }
}

const styles = StyleSheet.create({
    logo: {
        resizeMode: "cover",
        width: 130,
        height: 130,
        margin: 20,
    },
    input: {
        width: 240,
        height: 35,
        backgroundColor: '#83cfe3',
        margin: 10,
        padding: 8,
        color: 'white',
        borderRadius: 14,
        fontSize: 18,
        fontWeight: '500',
    },
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    text: {
        fontSize: 30,
        margin: 10,
        
    },
    text2: {
        fontSize: 20,
        margin: 10,
        
    },
    text3: {
        fontSize: 11,
        margin: 10,
        
    },
})