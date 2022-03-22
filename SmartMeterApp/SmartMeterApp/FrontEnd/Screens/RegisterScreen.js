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

export default class RegisterScreen extends React.Component {
    state = {
        username: '', password: '', family: '', reset_Q: '', reset_A: '', confirm_password: ','
    }
    onChangeText = (key, val) => {
        this.setState({ [key]: val })
    }
    signUp = async () => {
        const { username, password, family, reset_Q, reset_A, confirm_password } = this.state

        info = "uname="+this.state.username+"&pwd1="+this.state.password+"&pwd2="+this.state.confirm_password+"&family="+this.state.family+"&resetQ="+this.state.reset_Q+"&resetA="+this.state.reset_A;
        console.log(info);

        fetch("http://127.0.0.1:5000/register", {method: "POST",
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
                    Registration Center
                </Text>
            <TextInput
            style={styles.input}
            placeholder='Username'
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('username', val)}
            />
            <TextInput
            style={styles.input}
            placeholder='Password'
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
            <TextInput
            style={styles.input}
            placeholder='Family Size'
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('family', val)}
            />
            <TextInput
            style={styles.input}
            placeholder='Reset Question'
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('reset_Q', val)}
            />
            <TextInput
            style={styles.input}
            placeholder='Answer to Reset Question'
            autoCapitalize="none"
            placeholderTextColor='white'
            onChangeText={val => this.onChangeText('reset_A', val)}
            />
            <View style={{ flexDirection:"row" }}>
                <Button
                title='Sign Up'
                onPress={this.signUp}
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
})