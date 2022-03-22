using UnityEngine;

public class RotateCoin : MonoBehaviour
{
    public Vector3 rotationChange;
    public Transform transform_;
    
    void FixedUpdate()
    {
        transform_.eulerAngles += rotationChange*Time.deltaTime;
    }
}
