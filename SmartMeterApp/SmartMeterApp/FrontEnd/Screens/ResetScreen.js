import React from 'react'
import {
  View,
  Button,
  TextInput,
  StyleSheet,
  Image,
  Alert,
  Text
} from 'react-native'

export default class ResetScreen extends React.Component {
    state = {
        username: '', password: '', family: '', reset_Q: '', reset_A: '', confirm_password: ','
    }
    onChangeText = (key, val) => {
        this.setState({ [key]: val })
    }

    reset_question = async () => {
        info = "uname="+this.state.username;
        console.log(info)
        fetch("http://127.0.0.1:5000/reset_Q", {method: "POST",
            body: info, 
            header: {
                'Content-Type': 'application/json'
              } // <-- Post parameters        
        })
            .then((response) => response.json())
            .then((responseJson) => {
            console.log(responseJson);
            verification = responseJson.verification;

            if (verification == "False")
            {
                //navigation.navigate('NestedHome', { screen: 'Home' });
                
                Alert.alert("Invalid username. Cannot find a person with name"+this.state.username);
            }
            else
            {
                //navigation.navigate('Login');
                console.log("Happy!")
                this.setState({
                    reset_Q: responseJson.verification
                })
            }
            
        })
        .catch((error) => {
           console.error(error);
        });
     }

    confirm = async () => {
        const { username, password, family, reset_Q, reset_A, confirm_password } = this.state

        if (this.state.reset_Q == "")
        {
            Alert.alert("Get your reset question first.");
            return;
        }

        info = "uname="+this.state.username+"&pwd1="+this.state.password+"&pwd2="+this.state.confirm_password+"&resetQ="+this.state.reset_Q+"&resetA="+this.state.reset_A;
        console.log(info);

        fetch("http://127.0.0.1:5000/reset", {method: "POST",
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
                //navigation.navigate('NestedHome', { screen: 'Home' });
                console.log("Happy!")
                this.props.navigation.navigate('Login')
            }
            else if (verification == "Wrong answer")
            {
                Alert.alert("Wrong answer to the reset question!");
            }
            else if (verification == "Unmatched password and confirmation")
            {
                Alert.alert("Unmatched password and confirmation");
            }
            else
            {
                Alert.alert("Invalid password. A password should be composed of 5-15 characters with upper/lower case, number and special character (@$!%*#?&).");
                //navigation.navigate('Login');
            }
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
                    Account Reset Center
                </Text>
            <TextInput
            style={styles.input}
            placeholder='Username'
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('username', val)}
            />

            <Button
                title='Get Reset Question'
                onPress={this.reset_question}
            />

            <Text style={[styles.text2]}>
                    Your reset question: {this.state.reset_Q}
            </Text>
            <TextInput
            style={styles.input}
            placeholder='Answer to Reset Question'
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('reset_A', val)}
            />

            <TextInput
            style={styles.input}
            placeholder='New Password'
            secureTextEntry={true}
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('password', val)}
            />
            <TextInput
            style={styles.input}
            placeholder='Confirm Password'
            secureTextEntry={true}
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('confirm_password', val)}
            />

            <View style={{ flexDirection:"row" }}>
                <Button
                title='Confirm'
                onPress={this.confirm}
                />
                <Button
                title='Home'
                onPress={() => { this.props.navigation.navigate('Login') }}
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
        width: 350,
        height: 55,
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
})