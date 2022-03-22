using UnityEngine;

public class GetPowerup : MonoBehaviour
{
    public float powerupDuration;
    public float warningTime;
    public Material normalMaterial;
    public Material warningMaterial;
    public Material normalColor;
    public Material warningColor;
    bool currentMaterialIsNormal = true;
    private int numSwords = 0;

    void OnTriggerEnter(Collider collider)
    {
        if (collider.gameObject.tag == "Sword Power Up")
        {
            AudioManager.mainManager.Play("SwordSoundEffect");
            numSwords++;
            gameObject.GetComponent<CollideEnemy>().canDefeatEnemies = true;
            gameObject.transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().material = warningMaterial;
            gameObject.GetComponent<MeshRenderer>().material = warningColor;
            currentMaterialIsNormal = false;
            collider.gameObject.GetComponent<MeshRenderer>().enabled = false;
            collider.gameObject.GetComponent<BoxCollider>().enabled = false;
            Invoke("warningPowerup", powerupDuration-warningTime); 
            Invoke("stopPowerup", powerupDuration); 
        }
    }

    void stopPowerup()
    {
        if (numSwords == 0)
        {
            gameObject.GetComponent<CollideEnemy>().canDefeatEnemies = false;
        }
    }

    void warningPowerup()
    {
        numSwords--;
        if (numSwords > 0)
        {
            return;
        }
        transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().material = normalMaterial;
        gameObject.GetComponent<MeshRenderer>().material = normalColor;
        for (int i = 0; i < 3; i++)
        {
            Invoke("toggleMaterial", warningTime / 4 * (i + 1));
        }
    }

    void toggleMaterial()
    {
        if (numSwords > 0)
        {
            transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().material = warningMaterial; //
            gameObject.GetComponent<MeshRenderer>().material = warningColor; //
            currentMaterialIsNormal = false;
            return;
        }
        if (currentMaterialIsNormal)
        {
            transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().material = warningMaterial;
            gameObject.GetComponent<MeshRenderer>().material = warningColor;
        }
        else
        {
            transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().material = normalMaterial;
            gameObject.GetComponent<MeshRenderer>().material = normalColor;

        }
        currentMaterialIsNormal = !currentMaterialIsNormal;
    }
}
