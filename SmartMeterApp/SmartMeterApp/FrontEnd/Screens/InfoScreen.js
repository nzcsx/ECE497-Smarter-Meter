import React, { Component } from 'react'
import { View, Text, StyleSheet } from 'react-native'

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
});


class HttpExample extends Component {
   state = {
      data: ''
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
         </View>
      )
   }
}
export default HttpExample