import React, { Component } from 'react'
import { View, Text, StyleSheet, TextInput, Button, Alert } from 'react-native'

const styles = StyleSheet.create({
    bigBlack: {
        color: 'black',
        fontWeight: 'bold',
        fontSize: 19,
        backgroundColor: '#EFEFF4',
        alignItems: "center" ,
        justifyContent: "center",
    },
    smallBlack: {
        color: 'black',
        fontSize: 15,
        backgroundColor: '#EFEFF4',
        alignItems: "center" ,
        justifyContent: "center",
    },
    red: {
        color: 'red',
    },
    logo: {
        resizeMode: "cover",
        width: 130,
        height: 130,
        margin: 20,
    },
    input: {
        width: 170,
        height: 35,
        backgroundColor: '#83cfe3',
        margin: 10,
        padding: 8,
        color: 'white',
        borderRadius: 14,
        fontSize: 18,
        fontWeight: '500',
        alignItems: "center" ,
        justifyContent: "center",
    },
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    text: {
        fontWeight: 'bold',
        fontSize: 22,
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
});


class SurveyScreen extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: '',appliance:'', wattage:'', num:'', freq:'',
         }
    }

    onChangeText = (key, val) => {
        this.setState({ [key]: val })
    }
   
   componentDidMount = () => {
        fetch("http://127.0.0.1:5000/verify", {method: "POST",
            body: "uname=Lee", 
            header: {
                'Content-Type': 'application/json'
              } // <-- Post parameters        
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

    Refresh = async () => {
        fetch("http://127.0.0.1:5000/verify", {method: "POST",
        body: "uname=Lee", 
        header: {
            'Content-Type': 'application/json'
            } // <-- Post parameters        
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

    CheckAppliance = async () => {
        fetch("http://127.0.0.1:5000/checkAPP", {method: "POST",
        body: "uname=Lee", 
        header: {
            'Content-Type': 'application/json'
            } // <-- Post parameters        
        })
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson);
            Alert.alert("Inputted: ", responseJson.data);
        })
        .catch((error) => {
            console.error(error);
            Alert.alert("Inputted: ", responseJson.data);
        
        });
    }



    AddAppliance = async () => {
        //const { username, password, family, reset_Q, reset_A, confirm_password } = this.state

        info = "app="+this.state.appliance+"&wattage="+this.state.wattage+"&num="+this.state.num+"&freq="+this.state.freq;
        console.log(info);

        fetch("http://127.0.0.1:5000/addAPP", {method: "POST",
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
                this.setState({appliance:'', wattage:'', num:'', freq:'',});
                Alert.alert("Success");
            }
            else
            {
                Alert.alert("Invalid Input");
            }
        })
        .catch((error) => {
        console.error(error);
        });
    }

    ConfirmAppliance = async () => {
        //const { username, password, family, reset_Q, reset_A, confirm_password } = this.state

        info = "confirm";
        console.log(info);

        fetch("http://127.0.0.1:5000/confirmAPP", {method: "POST",
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

                Alert.alert("Successfully added all appliances! Please refresh to check.");
            }
            else
            {
                Alert.alert("Invalid Input");
            }
        })
        .catch((error) => {
        console.error(error);
        });
    }
   render() {
      return (
         <View style={{justifyContent: "center", alignItems: "center", flex: 1}}>
            <Text style={styles.bigBlack}>
               User name: {this.state.data.name}, UID: {this.state.data.id}
            </Text>
            <Text style={styles.bigBlack}>
               Your appliance information:
            </Text>
            <Text style={styles.smallBlack}>
               {this.state.data.appliance}
            </Text>
            <Text style={styles.smallBlack}>
               Your last data update time: {this.state.data.lastupdate}
            </Text>
            <Text style={styles.smallBlack}>
               Your last data login time: {this.state.data.lastlogin}
            </Text>
            <Text style={styles.text}>
               Update Your Appliance Information
            </Text>
            <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>
                <TextInput
                    style={styles.input}
                    placeholder='Appliance Name'
                    autoCapitalize="none"
                    placeholderTextColor='white'
                    onChangeText={val => this.onChangeText('appliance', val)}
                />
                <TextInput
                    style={styles.input}
                    placeholder='Wattage'
                    autoCapitalize="none"
                    placeholderTextColor='white'
                    onChangeText={val => this.onChangeText('wattage', val)}
                />
            </View>
            <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>
                <TextInput
                    style={styles.input}
                    placeholder='Number'
                    autoCapitalize="none"
                    placeholderTextColor='white'
                    onChangeText={val => this.onChangeText('num', val)}
                />
                <TextInput
                    style={styles.input}
                    placeholder='Freq'
                    autoCapitalize="none"
                    placeholderTextColor='white'
                    onChangeText={val => this.onChangeText('freq', val)}
                />
            </View>
            <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>
                <Button
                    title='Add Appliance'
                    onPress={this.AddAppliance}
                />

                <Button
                    title='Check my input'
                    onPress={this.CheckAppliance}
                />


            </View>
            <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>

                <Button
                    title='Confirm All'
                    onPress={this.ConfirmAppliance}
                />

                <Button
                    title='Refresh'
                    onPress={this.Refresh}
                />

                <Button
                    title='Home'
                    onPress={() => {this.props.navigation.navigate('NestedSettings') }}
                />
            </View>

         </View>
      )
   }
}

export default SurveyScreen