@Entity
@Table(name="poll")
public class Poll implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long mId;

    @Column(name="user_id")
    private long mUserId;

    @Column(name="question")
    private String mQuestion;

    @Column(name="date_created")
    private Date mDateCreated;
}